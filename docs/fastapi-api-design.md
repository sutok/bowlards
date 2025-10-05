# FastAPI API設計書

## 1. 概要

### 1.1 目的
Scoring Bowlards/BowlingアプリケーションのFastAPIバックエンドAPIの詳細設計を定義する。

### 1.2 API仕様
- **ベースURL**: `https://api.bowlards.com/api/v1`
- **認証方式**: Firebase JWT Token (Bearer Token)
- **データ形式**: JSON
- **文字エンコーディング**: UTF-8

## 2. 共通仕様

### 2.1 レスポンス形式

#### 成功レスポンス
```json
{
  "success": true,
  "data": {
    // レスポンスデータ
  },
  "meta": {
    "total": 100,
    "limit": 20,
    "offset": 0
  }
}
```

#### エラーレスポンス
```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Error message",
    "details": {}
  }
}
```

### 2.2 HTTPステータスコード

| コード | 説明 | 使用場面 |
|--------|------|----------|
| 200 | OK | 正常な取得・更新処理 |
| 201 | Created | リソース作成成功 |
| 400 | Bad Request | リクエスト形式エラー |
| 401 | Unauthorized | 認証エラー |
| 403 | Forbidden | 権限エラー |
| 404 | Not Found | リソース不存在 |
| 409 | Conflict | リソース重複 |
| 422 | Unprocessable Entity | バリデーションエラー |
| 500 | Internal Server Error | サーバー内部エラー |

### 2.3 認証ヘッダー

```http
Authorization: Bearer <Firebase_JWT_Token>
```

## 3. エンドポイント設計

### 3.1 ヘルスチェック

#### GET /
```http
GET /
```

**説明**: APIサーバーの稼働状況を確認

**認証**: 不要

**レスポンス**:
```json
{
  "success": true,
  "data": {
    "message": "Scoring Bowlards API",
    "version": "1.0.0",
    "status": "running"
  }
}
```

#### GET /health
```http
GET /health
```

**説明**: ヘルスチェック（詳細）

**認証**: 不要

**レスポンス**:
```json
{
  "success": true,
  "data": {
    "status": "healthy",
    "timestamp": "2024-01-01T00:00:00Z",
    "version": "1.0.0"
  }
}
```

### 3.2 ユーザー関連API

#### GET /users/profile
```http
GET /users/profile
Authorization: Bearer <token>
```

**説明**: 認証済みユーザーのプロフィール情報を取得

**認証**: 必要

**レスポンス**:
```json
{
  "success": true,
  "data": {
    "id": "user_123",
    "uid": "firebase_uid_123",
    "email": "user@example.com",
    "display_name": "John Doe",
    "photo_url": "https://example.com/photo.jpg",
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z"
  }
}
```

**エラー**:
- `401`: 認証エラー
- `404`: ユーザーが見つからない

#### PUT /users/profile
```http
PUT /users/profile
Authorization: Bearer <token>
Content-Type: application/json

{
  "display_name": "John Smith",
  "photo_url": "https://example.com/new-photo.jpg"
}
```

**説明**: 認証済みユーザーのプロフィール情報を更新

**認証**: 必要

**リクエストボディ**:
```json
{
  "display_name": "string (1-50文字)",
  "photo_url": "string (URL形式, オプション)"
}
```

**レスポンス**:
```json
{
  "success": true,
  "data": {
    "id": "user_123",
    "uid": "firebase_uid_123",
    "email": "user@example.com",
    "display_name": "John Smith",
    "photo_url": "https://example.com/new-photo.jpg",
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T12:00:00Z"
  }
}
```

**エラー**:
- `400`: バリデーションエラー
- `401`: 認証エラー
- `404`: ユーザーが見つからない

#### DELETE /users/profile
```http
DELETE /users/profile
Authorization: Bearer <token>
```

**説明**: 認証済みユーザーのアカウントを削除

**認証**: 必要

**レスポンス**:
```json
{
  "success": true,
  "data": {
    "message": "User deleted successfully"
  }
}
```

**エラー**:
- `401`: 認証エラー
- `404`: ユーザーが見つからない

### 3.3 ゲーム関連API

#### POST /games
```http
POST /games
Authorization: Bearer <token>
Content-Type: application/json

{}
```

**説明**: 新しいボーリングゲームを作成

**認証**: 必要

**リクエストボディ**: 空のオブジェクト（初期作成時）

**レスポンス**:
```json
{
  "success": true,
  "data": {
    "id": "game_123",
    "user_id": "user_123",
    "total_score": 0,
    "frames": [
      {
        "number": 1,
        "rolls": [],
        "score": 0,
        "is_strike": false,
        "is_spare": false,
        "is_completed": false
      },
      // ... 10フレーム分
    ],
    "status": "playing",
    "played_at": "2024-01-01T00:00:00Z",
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z"
  }
}
```

**エラー**:
- `401`: 認証エラー
- `404`: ユーザーが見つからない

#### GET /games/{id}
```http
GET /games/game_123
Authorization: Bearer <token>
```

**説明**: 指定されたゲームの詳細情報を取得

**認証**: 必要

**パスパラメータ**:
- `id`: ゲームID (string, required)

**レスポンス**:
```json
{
  "success": true,
  "data": {
    "id": "game_123",
    "user_id": "user_123",
    "total_score": 150,
    "frames": [
      {
        "number": 1,
        "rolls": [7, 3],
        "score": 20,
        "is_strike": false,
        "is_spare": true,
        "is_completed": true
      },
      // ... 他のフレーム
    ],
    "status": "playing",
    "played_at": "2024-01-01T00:00:00Z",
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:30:00Z"
  }
}
```

**エラー**:
- `401`: 認証エラー
- `403`: アクセス拒否（他のユーザーのゲーム）
- `404`: ゲームが見つからない

#### POST /games/{id}/roll
```http
POST /games/game_123/roll
Authorization: Bearer <token>
Content-Type: application/json

{
  "frame_number": 1,
  "pin_count": 7
}
```

**説明**: ゲームにロール（投球）を追加

**認証**: 必要

**パスパラメータ**:
- `id`: ゲームID (string, required)

**リクエストボディ**:
```json
{
  "frame_number": 1,  // フレーム番号 (1-10)
  "pin_count": 7      // 倒したピン数 (0-10)
}
```

**レスポンス**:
```json
{
  "success": true,
  "data": {
    "id": "game_123",
    "user_id": "user_123",
    "total_score": 20,
    "frames": [
      {
        "number": 1,
        "rolls": [7, 3],
        "score": 20,
        "is_strike": false,
        "is_spare": true,
        "is_completed": true
      },
      // ... 他のフレーム
    ],
    "status": "playing",
    "played_at": "2024-01-01T00:00:00Z",
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:30:00Z"
  }
}
```

**エラー**:
- `400`: バリデーションエラー、ゲーム完了済み
- `401`: 認証エラー
- `403`: アクセス拒否
- `404`: ゲームが見つからない

#### DELETE /games/{id}
```http
DELETE /games/game_123
Authorization: Bearer <token>
```

**説明**: 指定されたゲームを削除

**認証**: 必要

**パスパラメータ**:
- `id`: ゲームID (string, required)

**レスポンス**:
```json
{
  "success": true,
  "data": {
    "message": "Game deleted successfully"
  }
}
```

**エラー**:
- `401`: 認証エラー
- `403`: アクセス拒否
- `404`: ゲームが見つからない

#### GET /games/history
```http
GET /games/history?limit=20&offset=0&status=completed
Authorization: Bearer <token>
```

**説明**: ユーザーのゲーム履歴を取得（ページネーション対応）

**認証**: 必要

**クエリパラメータ**:
- `limit`: 取得件数 (integer, 1-100, default: 20)
- `offset`: オフセット (integer, >=0, default: 0)
- `status`: ステータスフィルター (string, "playing" | "completed", optional)

**レスポンス**:
```json
{
  "success": true,
  "data": [
    {
      "id": "game_123",
      "user_id": "user_123",
      "total_score": 150,
      "frames": [...],
      "status": "completed",
      "played_at": "2024-01-01T00:00:00Z",
      "created_at": "2024-01-01T00:00:00Z",
      "updated_at": "2024-01-01T00:30:00Z"
    },
    // ... 他のゲーム
  ],
  "meta": {
    "total": 50,
    "limit": 20,
    "offset": 0
  }
}
```

**エラー**:
- `400`: クエリパラメータエラー
- `401`: 認証エラー

#### GET /games/statistics
```http
GET /games/statistics
Authorization: Bearer <token>
```

**説明**: ユーザーのボーリング統計情報を取得

**認証**: 必要

**レスポンス**:
```json
{
  "success": true,
  "data": {
    "total_games": 25,
    "completed_games": 20,
    "average_score": 145.5,
    "highest_score": 280,
    "lowest_score": 89,
    "strike_count": 45,
    "spare_count": 32,
    "perfect_games": 1,
    "turkey_count": 3
  }
}
```

**エラー**:
- `401`: 認証エラー

## 4. データモデル

### 4.1 ユーザーモデル

```python
class UserResponse(BaseModel):
    id: str
    uid: str
    email: str
    display_name: str
    photo_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime
```

### 4.2 ゲームモデル

```python
class Frame(BaseModel):
    number: int = Field(..., ge=1, le=10)
    rolls: List[int] = Field(default_factory=list)
    score: int = 0
    is_strike: bool = False
    is_spare: bool = False
    is_completed: bool = False

class GameResponse(BaseModel):
    id: str
    user_id: str
    total_score: int
    frames: List[Frame]
    status: str
    played_at: datetime
    created_at: datetime
    updated_at: datetime
```

### 4.3 統計モデル

```python
class GameStatistics(BaseModel):
    total_games: int
    completed_games: int
    average_score: float
    highest_score: int
    lowest_score: int
    strike_count: int
    spare_count: int
    perfect_games: int
    turkey_count: int
```

## 5. バリデーションルール

### 5.1 ユーザー関連

| フィールド | ルール | エラーメッセージ |
|------------|--------|------------------|
| display_name | 1-50文字 | "Display name must be between 1 and 50 characters" |
| photo_url | URL形式 | "Photo URL must be a valid URL" |

### 5.2 ゲーム関連

| フィールド | ルール | エラーメッセージ |
|------------|--------|------------------|
| frame_number | 1-10 | "Frame number must be between 1 and 10" |
| pin_count | 0-10 | "Pin count must be between 0 and 10" |
| pin_count (1-9フレーム) | 0-10 | "Pin count cannot exceed 10 for frames 1-9" |
| pin_count (10フレーム) | 0-10 | "Pin count must be between 0 and 10" |

### 5.3 クエリパラメータ

| パラメータ | ルール | エラーメッセージ |
|------------|--------|------------------|
| limit | 1-100 | "Limit must be between 1 and 100" |
| offset | >=0 | "Offset must be 0 or greater" |
| status | "playing" \| "completed" | "Status must be 'playing' or 'completed'" |

## 6. エラーコード一覧

### 6.1 認証エラー

| コード | 説明 |
|--------|------|
| UNAUTHORIZED | 認証が必要 |
| INVALID_TOKEN | 無効なトークン |
| TOKEN_EXPIRED | トークン期限切れ |

### 6.2 バリデーションエラー

| コード | 説明 |
|--------|------|
| VALIDATION_ERROR | バリデーションエラー |
| INVALID_REQUEST | 無効なリクエスト |

### 6.3 リソースエラー

| コード | 説明 |
|--------|------|
| USER_NOT_FOUND | ユーザーが見つからない |
| GAME_NOT_FOUND | ゲームが見つからない |
| ACCESS_DENIED | アクセス拒否 |

### 6.4 ビジネスロジックエラー

| コード | 説明 |
|--------|------|
| GAME_COMPLETED | ゲームは既に完了済み |
| INVALID_ROLL | 無効なロール |
| FRAME_COMPLETED | フレームは既に完了済み |

## 7. レート制限

### 7.1 制限値

| エンドポイント | 制限 | 期間 |
|----------------|------|------|
| 全エンドポイント | 1000リクエスト | 1時間 |
| POST /games | 100リクエスト | 1時間 |
| POST /games/{id}/roll | 500リクエスト | 1時間 |

### 7.2 レート制限ヘッダー

```http
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1640995200
```

## 8. バージョニング

### 8.1 バージョン管理
- URLパスによるバージョニング (`/api/v1/`)
- 後方互換性の維持
- 非推奨APIの段階的廃止

### 8.2 バージョン情報
```http
GET /version
```

**レスポンス**:
```json
{
  "success": true,
  "data": {
    "version": "1.0.0",
    "api_version": "v1",
    "build_date": "2024-01-01T00:00:00Z"
  }
}
```

## 9. ドキュメント

### 9.1 Swagger UI
- URL: `/docs`
- インタラクティブなAPIドキュメント
- リクエスト/レスポンスの例

### 9.2 ReDoc
- URL: `/redoc`
- 読みやすいAPIドキュメント
- 詳細な仕様説明

## 10. テスト

### 10.1 テスト環境
- ベースURL: `https://api-dev.bowlards.com/api/v1`
- テスト用Firebaseプロジェクト
- モックデータの提供

### 10.2 テスト用エンドポイント
```http
POST /test/reset
```

**説明**: テストデータのリセット（テスト環境のみ）

---

このAPI設計書に基づいて、FastAPIバックエンドの実装を進めていきます。
