# FastAPIデータベース設計書（Firebase Firestore版）

## 1. 概要

### 1.1 データベース名
scoring-bawlards

### 1.2 設計の目的
ボーリングスコア記録・管理アプリケーション「Scoring Bowlards/Bowling」のFastAPIバックエンド用Firebase Firestoreデータベース設計。ユーザー情報、ゲーム記録、統計情報を効率的に管理し、TTL（Time To Live）による自動データ削除を実装する。

### 1.3 対象システム
- **バックエンド**: Python FastAPI
- **データベース**: Firebase Firestore
- **認証**: Firebase Authentication
- **ストレージ**: Firebase Storage（プロフィール画像用）
- **クラウド**: Google Cloud Platform (GCP)

## 2. データベース要件

### 2.1 機能要件
- **ユーザー管理**: Firebase認証との連携
- **ゲーム記録**: ボーリングゲームの詳細記録
- **スコア計算**: フレーム別スコアの管理
- **履歴管理**: 過去のゲーム履歴の保存（3ヶ月間）
- **統計情報**: ユーザー別統計データの管理
- **自動削除**: TTLによる3ヶ月後の自動データ削除

### 2.2 非機能要件
- **パフォーマンス**: レスポンス時間 < 100ms
- **可用性**: 99.95%以上
- **スケーラビリティ**: 10,000ユーザー対応
- **データ保持**: 3ヶ月間の履歴保持（TTL自動削除）
- **コスト最適化**: 無料枠内での運用

## 3. Firestoreコレクション設計

### 3.1 ユーザーコレクション (users)

#### 3.1.1 ドキュメント構造
```python
# コレクション: users
# ドキュメントID: Firebase UID
{
  "id": "firebase_uid_123",
  "uid": "firebase_uid_123",
  "email": "user@example.com",
  "display_name": "ユーザー名",
  "photo_url": "https://example.com/photo.jpg",
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

#### 3.1.2 Pydanticモデル
```python
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class UserSchema(BaseModel):
    id: str
    uid: str
    email: EmailStr
    display_name: str
    photo_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime

class UserCreate(BaseModel):
    uid: str
    email: EmailStr
    display_name: str
    photo_url: Optional[str] = None

class UserUpdate(BaseModel):
    display_name: Optional[str] = None
    photo_url: Optional[str] = None
```

#### 3.1.3 セキュリティルール
```javascript
// Firestore Security Rules
match /users/{userId} {
  allow read, write: if request.auth != null && request.auth.uid == userId;
}
```

### 3.2 ゲームコレクション (games)

#### 3.2.1 ドキュメント構造
```python
# コレクション: games
# ドキュメントID: 自動生成UUID
{
  "id": "game_uuid_123",
  "user_id": "firebase_uid_123",
  "total_score": 150,
  "status": "playing",  # "playing" | "completed"
  "frames": [
    {
      "number": 1,
      "rolls": [7, 3],
      "score": 20,
      "is_strike": False,
      "is_spare": True,
      "is_completed": True
    }
    # ... 10フレーム分
  ],
  "played_at": "2024-01-01T00:00:00Z",
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z",
  "expire_at": "2024-04-01T00:00:00Z"  # TTL用（3ヶ月後）
}
```

#### 3.2.2 Pydanticモデル
```python
from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import List, Optional

class Frame(BaseModel):
    number: int = Field(..., ge=1, le=10)
    rolls: List[int] = Field(default_factory=list)
    score: int = 0
    is_strike: bool = False
    is_spare: bool = False
    is_completed: bool = False

class GameSchema(BaseModel):
    id: str
    user_id: str
    total_score: int = 0
    frames: List[Frame] = Field(default_factory=list)
    status: str = "playing"
    played_at: datetime = Field(default_factory=datetime.now)
    created_at: datetime
    updated_at: datetime
    expire_at: datetime

class GameCreate(BaseModel):
    user_id: str
    total_score: int = 0
    frames: List[Frame] = Field(default_factory=list)
    status: str = "playing"
    played_at: datetime = Field(default_factory=datetime.now)

class RollRequest(BaseModel):
    frame_number: int = Field(..., ge=1, le=10)
    pin_count: int = Field(..., ge=0, le=10)
    
    @validator('pin_count')
    def validate_pin_count(cls, v, values):
        frame_number = values.get('frame_number')
        if frame_number < 10 and v > 10:
            raise ValueError('Pin count cannot exceed 10 for frames 1-9')
        return v
```

#### 3.2.3 セキュリティルール
```javascript
match /games/{gameId} {
  allow read, write: if request.auth != null && 
    request.auth.uid == resource.data.user_id;
  allow create: if request.auth != null && 
    request.auth.uid == request.resource.data.user_id;
}
```

### 3.3 ユーザー統計コレクション (user_statistics)

#### 3.3.1 ドキュメント構造
```python
# コレクション: user_statistics
# ドキュメントID: Firebase UID
{
  "id": "firebase_uid_123",
  "user_id": "firebase_uid_123",
  "total_games": 25,
  "completed_games": 20,
  "average_score": 145.5,
  "highest_score": 200,
  "lowest_score": 80,
  "strike_count": 15,
  "spare_count": 30,
  "perfect_games": 1,
  "turkey_count": 3,
  "last_updated": "2024-01-01T00:00:00Z",
  "created_at": "2024-01-01T00:00:00Z"
}
```

#### 3.3.2 Pydanticモデル
```python
class UserStatistics(BaseModel):
    id: str
    user_id: str
    total_games: int = 0
    completed_games: int = 0
    average_score: float = 0.0
    highest_score: int = 0
    lowest_score: int = 0
    strike_count: int = 0
    spare_count: int = 0
    perfect_games: int = 0
    turkey_count: int = 0
    last_updated: datetime
    created_at: datetime
```

## 4. TTL（Time To Live）設定

### 4.1 TTLポリシー設定
```python
# Firebase Admin SDK で設定
from google.cloud import firestore
from datetime import datetime, timedelta

def set_ttl_policy():
    """TTLポリシーを設定"""
    db = firestore.Client()
    
    # ゲームコレクションのTTL設定
    ttl_policy = {
        'collection': 'games',
        'field': 'expire_at',
        'ttl_days': 90  # 90日（3ヶ月）
    }
    
    return ttl_policy
```

### 4.2 データ作成時のTTL設定
```python
from datetime import datetime, timedelta

def create_game_with_ttl(user_id: str) -> dict:
    """TTL付きゲームデータを作成"""
    now = datetime.now()
    expire_at = now + timedelta(days=90)  # 3ヶ月後
    
    game_data = {
        'user_id': user_id,
        'total_score': 0,
        'status': 'playing',
        'frames': [],
        'played_at': now,
        'created_at': now,
        'updated_at': now,
        'expire_at': expire_at
    }
    
    return game_data
```

## 5. インデックス設計

### 5.1 複合インデックス
```python
# Firestore Console で設定
# コレクション: games
# フィールド: user_id (昇順), played_at (降順)
# 用途: ユーザー別ゲーム履歴取得

# コレクション: games  
# フィールド: user_id (昇順), status (昇順)
# 用途: ユーザー別進行中ゲーム取得

# コレクション: games
# フィールド: user_id (昇順), created_at (降順)
# 用途: ユーザー別ゲーム作成日時順取得
```

### 5.2 インデックス設定例
```json
{
  "indexes": [
    {
      "collectionGroup": "games",
      "queryScope": "COLLECTION",
      "fields": [
        {
          "fieldPath": "user_id",
          "order": "ASCENDING"
        },
        {
          "fieldPath": "played_at",
          "order": "DESCENDING"
        }
      ]
    },
    {
      "collectionGroup": "games",
      "queryScope": "COLLECTION",
      "fields": [
        {
          "fieldPath": "user_id",
          "order": "ASCENDING"
        },
        {
          "fieldPath": "status",
          "order": "ASCENDING"
        }
      ]
    }
  ]
}
```

## 6. セキュリティルール

### 6.1 完全なセキュリティルール
```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // ユーザー情報
    match /users/{userId} {
      allow read, write: if request.auth != null && 
        request.auth.uid == userId;
    }
    
    // ゲーム記録
    match /games/{gameId} {
      allow read, write: if request.auth != null && 
        request.auth.uid == resource.data.user_id;
      allow create: if request.auth != null && 
        request.auth.uid == request.resource.data.user_id;
    }
    
    // ユーザー統計
    match /user_statistics/{userId} {
      allow read, write: if request.auth != null && 
        request.auth.uid == userId;
    }
  }
}
```

## 7. FastAPI実装例

### 7.1 Firestoreクライアント設定
```python
# app/config.py
from google.cloud import firestore
from google.oauth2 import service_account
import os

class FirestoreConfig:
    def __init__(self):
        self.project_id = os.getenv("FIREBASE_PROJECT_ID")
        self.credentials_path = os.getenv("FIREBASE_CREDENTIALS_PATH")
        
    def get_client(self) -> firestore.Client:
        if self.credentials_path:
            credentials = service_account.Credentials.from_service_account_file(
                self.credentials_path
            )
            return firestore.Client(
                project=self.project_id,
                credentials=credentials
            )
        else:
            return firestore.Client(project=self.project_id)
```

### 7.2 リポジトリ実装例
```python
# app/repositories/game_repository.py
from google.cloud import firestore
from typing import List, Optional
from app.models.game import GameSchema, GameCreate
from datetime import datetime, timedelta

class GameRepository:
    def __init__(self, db: firestore.Client):
        self.db = db
        self.collection = "games"
    
    async def create(self, game_data: GameCreate) -> GameSchema:
        """ゲームを作成"""
        doc_ref = self.db.collection(self.collection).document()
        
        # TTL設定
        expire_at = datetime.now() + timedelta(days=90)
        
        game_dict = game_data.dict()
        game_dict['id'] = doc_ref.id
        game_dict['created_at'] = firestore.SERVER_TIMESTAMP
        game_dict['updated_at'] = firestore.SERVER_TIMESTAMP
        game_dict['expire_at'] = expire_at
        
        doc_ref.set(game_dict)
        return GameSchema(**game_dict)
    
    async def get_by_id(self, game_id: str, user_id: str) -> Optional[GameSchema]:
        """ゲームを取得"""
        doc = self.db.collection(self.collection).document(game_id).get()
        
        if not doc.exists:
            return None
        
        game_data = doc.to_dict()
        if game_data['user_id'] != user_id:
            return None
        
        return GameSchema(**game_data)
    
    async def get_user_games(
        self, 
        user_id: str, 
        limit: int = 20, 
        offset: int = 0,
        status: Optional[str] = None
    ) -> List[GameSchema]:
        """ユーザーのゲーム履歴を取得"""
        query = self.db.collection(self.collection).where("user_id", "==", user_id)
        
        if status:
            query = query.where("status", "==", status)
        
        query = query.order_by("played_at", direction=firestore.Query.DESCENDING)
        query = query.limit(limit).offset(offset)
        
        docs = query.stream()
        games = []
        
        for doc in docs:
            game_data = doc.to_dict()
            games.append(GameSchema(**game_data))
        
        return games
```

### 7.3 サービス実装例
```python
# app/services/game_service.py
from typing import List, Optional
from app.repositories.game_repository import GameRepository
from app.models.game import GameCreate, RollRequest, GameSchema
from app.utils.scoring import calculate_score

class GameService:
    def __init__(self, game_repo: GameRepository):
        self.game_repo = game_repo
    
    async def create_game(self, user_id: str) -> GameSchema:
        """新しいゲームを作成"""
        # 10フレームを初期化
        frames = []
        for i in range(10):
            frames.append({
                'number': i + 1,
                'rolls': [],
                'score': 0,
                'is_strike': False,
                'is_spare': False,
                'is_completed': False
            })
        
        game_data = GameCreate(
            user_id=user_id,
            frames=frames
        )
        
        return await self.game_repo.create(game_data)
    
    async def add_roll(
        self, 
        game_id: str, 
        user_id: str, 
        roll: RollRequest
    ) -> GameSchema:
        """ロールを追加してスコアを計算"""
        game = await self.game_repo.get_by_id(game_id, user_id)
        if not game:
            raise ValueError("Game not found")
        
        # スコア計算ロジック
        updated_game = calculate_score(game, roll)
        
        # データベース更新
        return await self.game_repo.update(game_id, updated_game)
```

## 8. コスト最適化

### 8.1 無料枠内での運用
```python
# 月間想定使用量（100ユーザー、500ゲーム）
monthly_usage = {
    'storage': '0.5GB',  # 無料枠: 1GB
    'reads': '10,000',   # 無料枠: 50,000
    'writes': '8,000',   # 無料枠: 20,000
    'deletes': '6,000'   # 無料枠: 20,000
}
```

### 8.2 クエリ最適化
```python
# 効率的なクエリ例
def get_user_games_optimized(user_id: str, limit: int = 20):
    """最適化されたユーザーゲーム取得"""
    query = (
        db.collection('games')
        .where('user_id', '==', user_id)
        .order_by('played_at', direction=firestore.Query.DESCENDING)
        .limit(limit)
    )
    return query.stream()
```

## 9. 監視・ログ

### 9.1 データベース監視
```python
# app/utils/monitoring.py
import logging
from google.cloud import firestore

logger = logging.getLogger(__name__)

class FirestoreMonitor:
    def __init__(self, db: firestore.Client):
        self.db = db
    
    def log_query_performance(self, query_name: str, execution_time: float):
        """クエリパフォーマンスをログ出力"""
        logger.info(f"Query {query_name} executed in {execution_time:.2f}s")
    
    def log_data_usage(self, collection: str, operation: str):
        """データ使用量をログ出力"""
        logger.info(f"Operation {operation} on collection {collection}")
```

## 10. テスト

### 10.1 単体テスト例
```python
# tests/test_game_repository.py
import pytest
from unittest.mock import Mock, patch
from app.repositories.game_repository import GameRepository
from app.models.game import GameCreate

@pytest.fixture
def mock_firestore():
    return Mock()

@pytest.fixture
def game_repository(mock_firestore):
    return GameRepository(mock_firestore)

async def test_create_game(game_repository, mock_firestore):
    """ゲーム作成テスト"""
    # モック設定
    mock_doc_ref = Mock()
    mock_doc_ref.id = "test_game_id"
    mock_doc_ref.set = Mock()
    mock_firestore.collection.return_value.document.return_value = mock_doc_ref
    
    # テスト実行
    game_data = GameCreate(user_id="test_user")
    result = await game_repository.create(game_data)
    
    # 検証
    assert result.id == "test_game_id"
    assert result.user_id == "test_user"
    mock_doc_ref.set.assert_called_once()
```

## 11. 変更履歴

| バージョン | 日付 | 変更内容 | 担当者 |
|-----------|------|----------|--------|
| 3.0.0 | 2024-01-01 | FastAPI対応、Python実装例追加 | システムエンジニア |
| 2.0.0 | 2024-09-19 | Firebase Firestore版に移行、TTL機能追加 | システムエンジニア |

---

**注意事項**:
- 本設計書はFastAPIとFirebase Firestoreの特性を考慮した設計
- TTL機能により3ヶ月後の自動削除を実装
- 無料枠内での運用を前提としたコスト最適化
- セキュリティルールによる適切なアクセス制御
- Pythonの型ヒントとPydanticによる型安全性の確保
