# FastAPI Firebase認証設計書

## 1. 概要

### 1.1 機能名
Firebase Authentication System for FastAPI

### 1.2 機能の目的
Scoring Bowlards/Bowlingアプリケーションにおいて、FastAPIバックエンドでユーザーの認証・認可を管理し、セキュアなアクセス制御を提供する。

### 1.3 対象システム
- **アプリケーション名**: Scoring Bowlards/Bowling
- **フロントエンド**: React + Redux
- **バックエンド**: Python FastAPI
- **認証プロバイダー**: Firebase Authentication
- **クラウドプラットフォーム**: Google Cloud Platform (GCP)

## 2. 認証方式

### 2.1 認証プロバイダー
- **Google認証**: プライマリ認証方式
- **メール/パスワード認証**: セカンダリ認証方式（オプション）

### 2.2 認証フロー
```mermaid
sequenceDiagram
    participant U as ユーザー
    participant F as フロントエンド(React)
    participant FB as Firebase Auth
    participant B as バックエンド(FastAPI)
    participant G as Google API

    U->>F: ログイン要求
    F->>FB: 認証要求
    FB->>G: Google認証
    G-->>FB: 認証トークン
    FB-->>F: Firebase ID Token
    F->>B: API呼び出し(ID Token付き)
    B->>FB: トークン検証
    FB-->>B: 検証結果
    B-->>F: 認証済みレスポンス
    F-->>U: 認証完了
```

## 3. FastAPI認証実装

### 3.1 依存関係の設定

#### 3.1.1 requirements.txt
```txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
firebase-admin==6.2.0
python-jose[cryptography]==3.3.0
python-multipart==0.0.6
pydantic==2.5.0
pydantic-settings==2.1.0
```

#### 3.1.2 Firebase設定
```python
# app/config.py
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Firebase設定
    firebase_project_id: str
    firebase_credentials_path: Optional[str] = None
    firebase_private_key: Optional[str] = None
    firebase_client_email: Optional[str] = None
    
    class Config:
        env_file = ".env"
        env_prefix = "APP_"

settings = Settings()
```

### 3.2 Firebase認証クライアント

#### 3.2.1 Firebase初期化
```python
# app/auth/firebase.py
import firebase_admin
from firebase_admin import credentials, auth
from google.oauth2 import service_account
import os
from app.config import settings

class FirebaseAuth:
    def __init__(self):
        self._initialize_firebase()
    
    def _initialize_firebase(self):
        """Firebase Admin SDKを初期化"""
        if not firebase_admin._apps:
            if settings.firebase_credentials_path:
                # サービスアカウントキーファイルから認証情報を読み込み
                cred = credentials.Certificate(settings.firebase_credentials_path)
                firebase_admin.initialize_app(cred)
            elif settings.firebase_private_key and settings.firebase_client_email:
                # 環境変数から認証情報を読み込み
                cred_dict = {
                    "type": "service_account",
                    "project_id": settings.firebase_project_id,
                    "private_key": settings.firebase_private_key.replace('\\n', '\n'),
                    "client_email": settings.firebase_client_email,
                    "token_uri": "https://oauth2.googleapis.com/token"
                }
                cred = credentials.Certificate(cred_dict)
                firebase_admin.initialize_app(cred)
            else:
                # デフォルト認証（Cloud Runやローカル開発環境のエミュレータ用）
                firebase_admin.initialize_app()
    
    async def verify_token(self, token: str) -> dict:
        """Firebase IDトークンを検証"""
        try:
            decoded_token = auth.verify_id_token(token)
            return decoded_token
        except auth.InvalidIdTokenError:
            raise ValueError("Invalid ID token")
        except auth.ExpiredIdTokenError:
            raise ValueError("Expired ID token")
        except Exception as e:
            raise ValueError(f"Token verification failed: {str(e)}")

# シングルトンインスタンス
firebase_auth = FirebaseAuth()
```

### 3.3 認証依存関係

#### 3.3.1 認証依存関係
```python
# app/auth/dependencies.py
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.auth.firebase import firebase_auth
from typing import Dict, Any

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> Dict[str, Any]:
    """現在のユーザーを取得"""
    try:
        token = credentials.credentials
        decoded_token = await firebase_auth.verify_token(token)
        return decoded_token
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Authentication failed: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )

async def get_current_user_id(
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> str:
    """現在のユーザーIDを取得"""
    return current_user.get("uid")

async def get_current_user_email(
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> str:
    """現在のユーザーメールアドレスを取得"""
    return current_user.get("email")
```

### 3.4 認証ミドルウェア

#### 3.4.1 カスタムミドルウェア
```python
# app/middleware.py
from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
import time
import logging

logger = logging.getLogger(__name__)

class AuthMiddleware:
    def __init__(self, app):
        self.app = app
    
    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            request = Request(scope, receive)
            
            # 認証が必要なパスをチェック
            if self._requires_auth(request.url.path):
                auth_header = request.headers.get("authorization")
                if not auth_header or not auth_header.startswith("Bearer "):
                    response = JSONResponse(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        content={
                            "success": False,
                            "error": {
                                "code": "UNAUTHORIZED",
                                "message": "Authorization header required"
                            }
                        }
                    )
                    await response(scope, receive, send)
                    return
        
        await self.app(scope, receive, send)
    
    def _requires_auth(self, path: str) -> bool:
        """認証が必要なパスかどうかを判定"""
        public_paths = [
            "/",
            "/health",
            "/docs",
            "/redoc",
            "/openapi.json"
        ]
        return not any(path.startswith(p) for p in public_paths)
```

### 3.5 認証エラーハンドリング

#### 3.5.1 カスタム例外
```python
# app/exceptions.py
from fastapi import HTTPException, status

class AuthenticationError(HTTPException):
    def __init__(self, detail: str = "Authentication failed"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail
        )

class AuthorizationError(HTTPException):
    def __init__(self, detail: str = "Access denied"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail
        )

class TokenExpiredError(HTTPException):
    def __init__(self, detail: str = "Token expired"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail
        )
```

#### 3.5.2 グローバル例外ハンドラー
```python
# app/main.py
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.exceptions import AuthenticationError, AuthorizationError, TokenExpiredError

app = FastAPI()

@app.exception_handler(AuthenticationError)
async def authentication_exception_handler(request: Request, exc: AuthenticationError):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "code": "AUTHENTICATION_ERROR",
                "message": exc.detail
            }
        }
    )

@app.exception_handler(AuthorizationError)
async def authorization_exception_handler(request: Request, exc: AuthorizationError):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "code": "AUTHORIZATION_ERROR",
                "message": exc.detail
            }
        }
    )

@app.exception_handler(TokenExpiredError)
async def token_expired_exception_handler(request: Request, exc: TokenExpiredError):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "code": "TOKEN_EXPIRED",
                "message": exc.detail
            }
        }
    )
```

## 4. API実装例

### 4.1 認証が必要なエンドポイント

#### 4.1.1 ユーザープロフィール取得
```python
# app/routers/users.py
from fastapi import APIRouter, Depends, HTTPException, status
from app.auth.dependencies import get_current_user, get_current_user_id
from app.models.user import UserResponse
from app.services.user_service import UserService
from typing import Dict, Any

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/profile", response_model=UserResponse)
async def get_user_profile(
    current_user: Dict[str, Any] = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service)
):
    """ユーザープロフィールを取得"""
    try:
        user_id = current_user.get("uid")
        user = await user_service.get_user_profile(user_id)
        return user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
```

#### 4.1.2 ゲーム作成
```python
# app/routers/games.py
from fastapi import APIRouter, Depends, HTTPException, status
from app.auth.dependencies import get_current_user_id
from app.models.game import GameResponse
from app.services.game_service import GameService

router = APIRouter(prefix="/games", tags=["games"])

@router.post("/", response_model=GameResponse)
async def create_game(
    user_id: str = Depends(get_current_user_id),
    game_service: GameService = Depends(get_game_service)
):
    """新しいゲームを作成"""
    try:
        game = await game_service.create_game(user_id)
        return game
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create game"
        )
```

### 4.2 認証が不要なエンドポイント

#### 4.2.1 ヘルスチェック
```python
# app/main.py
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    """ルートエンドポイント"""
    return {
        "success": True,
        "data": {
            "message": "Scoring Bowlards API",
            "version": "1.0.0",
            "status": "running"
        }
    }

@app.get("/health")
async def health_check():
    """ヘルスチェック"""
    return {
        "success": True,
        "data": {
            "status": "healthy",
            "timestamp": "2024-01-01T00:00:00Z"
        }
    }
```

## 5. セキュリティ対策

### 5.1 トークン管理
- **ID Token有効期限**: 1時間
- **Refresh Token**: 自動更新
- **トークン検証**: Firebase Admin SDKを使用

### 5.2 セキュリティヘッダー
```python
# app/middleware.py
from fastapi import Request
from fastapi.responses import Response

class SecurityHeadersMiddleware:
    def __init__(self, app):
        self.app = app
    
    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            request = Request(scope, receive)
            
            async def send_wrapper(message):
                if message["type"] == "http.response.start":
                    headers = dict(message.get("headers", []))
                    headers.extend([
                        (b"x-content-type-options", b"nosniff"),
                        (b"x-frame-options", b"DENY"),
                        (b"x-xss-protection", b"1; mode=block"),
                        (b"strict-transport-security", b"max-age=31536000; includeSubDomains"),
                    ])
                    message["headers"] = list(headers.items())
                await send(message)
            
            await self.app(scope, receive, send_wrapper)
        else:
            await self.app(scope, receive, send)
```

### 5.3 レート制限
```python
# app/middleware.py
from collections import defaultdict
import time

class RateLimitMiddleware:
    def __init__(self, app, calls: int = 100, period: int = 3600):
        self.app = app
        self.calls = calls
        self.period = period
        self.clients = defaultdict(list)
    
    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            request = Request(scope, receive)
            client_ip = request.client.host
            
            # レート制限チェック
            now = time.time()
            client_calls = self.clients[client_ip]
            
            # 古い呼び出しを削除
            client_calls[:] = [call_time for call_time in client_calls if now - call_time < self.period]
            
            if len(client_calls) >= self.calls:
                response = JSONResponse(
                    status_code=429,
                    content={
                        "success": False,
                        "error": {
                            "code": "RATE_LIMIT_EXCEEDED",
                            "message": "Too many requests"
                        }
                    }
                )
                await response(scope, receive, send)
                return
            
            # 呼び出しを記録
            client_calls.append(now)
        
        await self.app(scope, receive, send)
```

## 6. テスト実装

### 6.1 認証テスト
```python
# tests/test_auth.py
import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch
from app.main import app

client = TestClient(app)

@pytest.fixture
def mock_firebase_auth():
    with patch('app.auth.firebase.firebase_auth') as mock:
        yield mock

def test_authenticated_endpoint_success(mock_firebase_auth):
    """認証済みエンドポイントの成功テスト"""
    # モック設定
    mock_firebase_auth.verify_token.return_value = {
        "uid": "test_user_id",
        "email": "test@example.com"
    }
    
    # テスト実行
    response = client.get(
        "/users/profile",
        headers={"Authorization": "Bearer test_token"}
    )
    
    # 検証
    assert response.status_code == 200

def test_authenticated_endpoint_no_token():
    """トークンなしでのアクセステスト"""
    response = client.get("/users/profile")
    assert response.status_code == 401

def test_authenticated_endpoint_invalid_token(mock_firebase_auth):
    """無効なトークンでのアクセステスト"""
    # モック設定
    mock_firebase_auth.verify_token.side_effect = ValueError("Invalid token")
    
    # テスト実行
    response = client.get(
        "/users/profile",
        headers={"Authorization": "Bearer invalid_token"}
    )
    
    # 検証
    assert response.status_code == 401
    assert response.json()["error"]["code"] == "AUTHENTICATION_ERROR"
```

### 6.2 統合テスト
```python
# tests/test_integration.py
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    """ヘルスチェックテスト"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["success"] is True

def test_root_endpoint():
    """ルートエンドポイントテスト"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["data"]["message"] == "Scoring Bowlards API"
```

## 7. 環境変数設定

### 7.1 環境変数
```bash
# Firebase設定
APP_FIREBASE_PROJECT_ID=your-project-id
APP_FIREBASE_CREDENTIALS_PATH=/path/to/credentials.json
# または
APP_FIREBASE_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n"
APP_FIREBASE_CLIENT_EMAIL=your-service-account@your-project.iam.gserviceaccount.com

# サーバー設定
APP_HOST=0.0.0.0
APP_PORT=8000
APP_DEBUG=false

# ログ設定
APP_LOG_LEVEL=INFO
APP_LOG_FORMAT=json
```

### 7.2 .env.example
```bash
# Firebase設定
APP_FIREBASE_PROJECT_ID=bowlards-dev
APP_FIREBASE_CREDENTIALS_PATH=./credentials.json

# サーバー設定
APP_HOST=0.0.0.0
APP_PORT=8000
APP_DEBUG=false

# ログ設定
APP_LOG_LEVEL=INFO
APP_LOG_FORMAT=json
```

## 8. 監視・ログ

### 8.1 認証ログ
```python
# app/utils/logging.py
import logging
import structlog
from typing import Dict, Any

logger = structlog.get_logger()

class AuthLogger:
    @staticmethod
    def log_authentication_success(user_id: str, email: str):
        """認証成功ログ"""
        logger.info(
            "Authentication successful",
            user_id=user_id,
            email=email,
            event="auth_success"
        )
    
    @staticmethod
    def log_authentication_failure(error: str, user_id: str = None):
        """認証失敗ログ"""
        logger.warning(
            "Authentication failed",
            error=error,
            user_id=user_id,
            event="auth_failure"
        )
    
    @staticmethod
    def log_token_verification(token: str, success: bool):
        """トークン検証ログ"""
        logger.info(
            "Token verification",
            success=success,
            event="token_verification"
        )
```

### 8.2 メトリクス
```python
# app/utils/metrics.py
from prometheus_client import Counter, Histogram
import time

# 認証関連メトリクス
auth_attempts = Counter('auth_attempts_total', 'Total authentication attempts', ['status'])
auth_duration = Histogram('auth_duration_seconds', 'Authentication duration')

def track_auth_attempt(success: bool):
    """認証試行を追跡"""
    status = 'success' if success else 'failure'
    auth_attempts.labels(status=status).inc()

def track_auth_duration(func):
    """認証処理時間を追跡"""
    def wrapper(*args, **kwargs):
        with auth_duration.time():
            return func(*args, **kwargs)
    return wrapper
```

## 9. 変更履歴

| バージョン | 日付 | 変更内容 | 担当者 |
|-----------|------|----------|--------|
| 2.0.0 | 2024-01-01 | FastAPI対応、Python実装例追加 | システムエンジニア |
| 1.0.0 | 2024-01-01 | 初版作成 | システムエンジニア |

---

**注意事項**:
- 本設計書はFastAPIとFirebase Authenticationの特性を考慮した設計
- セキュリティ要件の変更時は、必ず設計書を更新すること
- 新しい認証プロバイダーの追加時は、本設計書を拡張すること
- 本番環境では適切なログ監視とアラート設定を行うこと
