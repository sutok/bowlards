# API設計書（Firebase Firestore版）

## 1. 概要

### 1.1 API名
Scoring Bawlards/Bowling API

### 1.2 APIの目的
ボーリングスコア記録・管理アプリケーションのRESTful API。Firebase Firestoreを使用し、ユーザー認証、ゲーム記録管理、統計情報提供を行う。

### 1.3 対象システム
- **フレームワーク**: Echo (Go)
- **認証**: Firebase Authentication
- **データベース**: Firebase Firestore
- **API仕様**: RESTful API v1

## 2. API基本仕様

### 2.1 ベースURL
```
開発環境: http://localhost:18080/api/v1
本番環境: https://api.bowlards.com/api/v1
```

### 2.2 認証方式
- **認証方法**: Firebase ID Token
- **ヘッダー**: `Authorization: Bearer <firebase_id_token>`
- **トークン有効期限**: 1時間
- **自動更新**: フロントエンドで実装

### 2.3 共通レスポンス形式

#### 2.3.1 成功レスポンス
```json
{
  "success": true,
  "data": {
    // レスポンスデータ
  },
  "meta": {
    "timestamp": "2024-01-01T00:00:00Z",
    "pagination": {
      "currentPage": 1,
      "totalPages": 10,
      "totalItems": 100,
      "itemsPerPage": 10,
      "hasNextPage": true,
      "hasPreviousPage": false
    }
  }
}
```

#### 2.3.2 エラーレスポンス
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "details": "Field 'email' is required"
  },
  "meta": {
    "timestamp": "2024-01-01T00:00:00Z"
  }
}
```

## 3. 認証関連API

### 3.1 ユーザープロフィール取得

#### 3.1.1 エンドポイント
```
GET /api/v1/user/profile
```

#### 3.1.2 リクエスト
```http
GET /api/v1/user/profile HTTP/1.1
Authorization: Bearer <firebase_id_token>
Content-Type: application/json
```

#### 3.1.3 レスポンス
```json
{
  "success": true,
  "data": {
    "uid": "firebase_uid_123",
    "email": "user@example.com",
    "displayName": "田中太郎",
    "photoURL": "https://example.com/photo.jpg",
    "emailVerified": true,
    "createdAt": "2024-01-01T00:00:00Z",
    "updatedAt": "2024-01-01T00:00:00Z"
  }
}
```

## 4. ゲーム関連API

### 4.1 ゲーム作成

#### 4.1.1 エンドポイント
```
POST /api/v1/games
```

#### 4.1.2 リクエスト
```json
{
  "gameDate": "2024-01-01T10:00:00Z"
}
```

#### 4.1.3 レスポンス
```json
{
  "success": true,
  "data": {
    "game": {
      "id": "game_uuid_123",
      "userId": "firebase_uid_123",
      "gameDate": "2024-01-01T10:00:00Z",
      "totalScore": 0,
      "status": "in_progress",
      "frames": [],
      "statistics": {
        "strikeCount": 0,
        "spareCount": 0,
        "averageScore": 0
      },
      "createdAt": "2024-01-01T10:00:00Z",
      "updatedAt": "2024-01-01T10:00:00Z",
      "expireAt": "2024-04-01T10:00:00Z"
    }
  }
}
```

### 4.2 ゲーム詳細取得

#### 4.2.1 エンドポイント
```
GET /api/v1/games/{gameId}
```

#### 4.2.2 レスポンス
```json
{
  "success": true,
  "data": {
    "game": {
      "id": "game_uuid_123",
      "userId": "firebase_uid_123",
      "gameDate": "2024-01-01T10:00:00Z",
      "totalScore": 150,
      "status": "completed",
      "frames": [
        {
          "frameNumber": 1,
          "firstRoll": 10,
          "secondRoll": null,
          "thirdRoll": null,
          "frameScore": 19,
          "isStrike": true,
          "isSpare": false,
          "isCompleted": true
        }
      ],
      "statistics": {
        "strikeCount": 3,
        "spareCount": 2,
        "averageScore": 150.0
      },
      "createdAt": "2024-01-01T10:00:00Z",
      "updatedAt": "2024-01-01T10:30:00Z",
      "expireAt": "2024-04-01T10:00:00Z"
    }
  }
}
```

### 4.3 フレーム更新

#### 4.3.1 エンドポイント
```
POST /api/v1/games/{gameId}/frames
```

#### 4.3.2 リクエスト
```json
{
  "frameNumber": 1,
  "rollNumber": 1,
  "pins": 10
}
```

#### 4.3.3 レスポンス
```json
{
  "success": true,
  "data": {
    "frame": {
      "frameNumber": 1,
      "firstRoll": 10,
      "secondRoll": null,
      "thirdRoll": null,
      "frameScore": null,
      "isStrike": true,
      "isSpare": false,
      "isCompleted": false
    },
    "game": {
      "id": "game_uuid_123",
      "totalScore": 0,
      "status": "in_progress"
    }
  }
}
```

## 5. 履歴関連API

### 5.1 ゲーム履歴一覧取得

#### 5.1.1 エンドポイント
```
GET /api/v1/games/history
```

#### 5.1.2 クエリパラメータ
- **page**: ページ番号（デフォルト: 1）
- **limit**: 1ページあたりの件数（デフォルト: 10、最大: 50）
- **dateFrom**: 開始日（ISO 8601形式）
- **dateTo**: 終了日（ISO 8601形式）
- **minScore**: 最小スコア
- **maxScore**: 最大スコア

#### 5.1.3 レスポンス
```json
{
  "success": true,
  "data": {
    "games": [
      {
        "id": "game_uuid_123",
        "gameDate": "2024-01-01T10:00:00Z",
        "totalScore": 150,
        "strikes": 3,
        "spares": 2,
        "status": "completed",
        "duration": 45
      }
    ],
    "pagination": {
      "currentPage": 1,
      "totalPages": 5,
      "totalItems": 50,
      "itemsPerPage": 10,
      "hasNextPage": true,
      "hasPreviousPage": false
    }
  }
}
```

### 5.2 統計情報取得

#### 5.2.1 エンドポイント
```
GET /api/v1/games/statistics
```

#### 5.2.2 レスポンス
```json
{
  "success": true,
  "data": {
    "statistics": {
      "totalGames": 25,
      "averageScore": 142.5,
      "highestScore": 200,
      "lowestScore": 89,
      "totalStrikes": 45,
      "totalSpares": 32,
      "gamesThisMonth": 8,
      "improvementRate": 5.2,
      "lastUpdated": "2024-01-01T10:00:00Z"
    }
  }
}
```

## 6. Firebase Firestore統合

### 6.1 データ操作パターン

#### 6.1.1 ゲーム作成
```go
// Firestoreにゲームを作成
func createGame(userID string, gameDate time.Time) (*Game, error) {
    gameData := map[string]interface{}{
        "userId": userID,
        "gameDate": gameDate,
        "totalScore": 0,
        "status": "in_progress",
        "frames": []interface{}{},
        "statistics": map[string]interface{}{
            "strikeCount": 0,
            "spareCount": 0,
            "averageScore": 0,
        },
        "createdAt": time.Now(),
        "updatedAt": time.Now(),
        "expireAt": time.Now().AddDate(0, 0, 90), // 3ヶ月後
    }
    
    docRef, _, err := client.Collection("games").Add(ctx, gameData)
    if err != nil {
        return nil, err
    }
    
    return &Game{
        ID: docRef.ID,
        // ... その他のフィールド
    }, nil
}
```

#### 6.1.2 ゲーム取得
```go
// Firestoreからゲームを取得
func getGame(gameID string) (*Game, error) {
    doc, err := client.Collection("games").Doc(gameID).Get(ctx)
    if err != nil {
        return nil, err
    }
    
    var game Game
    if err := doc.DataTo(&game); err != nil {
        return nil, err
    }
    
    return &game, nil
}
```

#### 6.1.3 ゲーム履歴取得
```go
// Firestoreからユーザーのゲーム履歴を取得
func getGameHistory(userID string, limit int, offset int) ([]*Game, error) {
    query := client.Collection("games").
        Where("userId", "==", userID).
        OrderBy("gameDate", firestore.Desc).
        Limit(limit).
        Offset(offset)
    
    docs, err := query.Documents(ctx).GetAll()
    if err != nil {
        return nil, err
    }
    
    var games []*Game
    for _, doc := range docs {
        var game Game
        if err := doc.DataTo(&game); err != nil {
            continue
        }
        games = append(games, &game)
    }
    
    return games, nil
}
```

### 6.2 TTL（Time To Live）実装

#### 6.2.1 TTLポリシー設定
```go
// Firebase Admin SDKでTTLポリシーを設定
func setupTTLPolicy() error {
    ttlPolicy := &firestore.TTLPolicy{
        Field: "expireAt",
        TTL:   90 * 24 * time.Hour, // 90日
    }
    
    _, err := client.Collection("games").Doc("_ttl_policy").Set(ctx, map[string]interface{}{
        "ttl": ttlPolicy,
    })
    
    return err
}
```

#### 6.2.2 データ作成時のTTL設定
```go
// ゲーム作成時にTTLを設定
func createGameWithTTL(userID string, gameDate time.Time) (*Game, error) {
    expireAt := time.Now().AddDate(0, 0, 90) // 3ヶ月後
    
    gameData := map[string]interface{}{
        "userId": userID,
        "gameDate": gameDate,
        "expireAt": expireAt,
        // ... その他のフィールド
    }
    
    docRef, _, err := client.Collection("games").Add(ctx, gameData)
    if err != nil {
        return nil, err
    }
    
    return &Game{ID: docRef.ID}, nil
}
```

## 7. エラーコード一覧

### 7.1 認証エラー
- **UNAUTHORIZED**: 認証が必要
- **INVALID_TOKEN**: 無効なトークン
- **TOKEN_EXPIRED**: トークン期限切れ
- **FORBIDDEN**: アクセス権限なし

### 7.2 Firestoreエラー
- **FIRESTORE_ERROR**: Firestore操作エラー
- **DOCUMENT_NOT_FOUND**: ドキュメントが見つからない
- **PERMISSION_DENIED**: 権限不足
- **QUOTA_EXCEEDED**: クォータ超過

### 7.3 バリデーションエラー
- **VALIDATION_ERROR**: バリデーションエラー
- **REQUIRED_FIELD**: 必須フィールドが不足
- **INVALID_FORMAT**: 無効な形式
- **OUT_OF_RANGE**: 範囲外の値

## 8. セキュリティ

### 8.1 Firestoreセキュリティルール
```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // ゲーム記録
    match /games/{gameId} {
      allow read, write: if request.auth != null && 
        request.auth.uid == resource.data.userId;
      allow create: if request.auth != null && 
        request.auth.uid == request.resource.data.userId;
    }
    
    // ユーザー統計
    match /userStatistics/{userId} {
      allow read, write: if request.auth != null && 
        request.auth.uid == userId;
    }
  }
}
```

### 8.2 CORS設定
```go
AllowedOrigins: []string{
    "http://localhost:13000",
    "https://bowlards.com"
}
AllowedMethods: []string{"GET", "POST", "PUT", "DELETE", "OPTIONS"}
AllowedHeaders: []string{"Authorization", "Content-Type"}
```

## 9. コスト最適化

### 9.1 無料枠内での運用
```go
// 月間想定使用量（100ユーザー、500ゲーム）
const monthlyUsage = {
    storage: "0.5GB",    // 無料枠: 1GB
    reads: "10,000",     // 無料枠: 50,000
    writes: "8,000",     // 無料枠: 20,000
    deletes: "6,000"     // 無料枠: 20,000
}
```

### 9.2 クエリ最適化
```go
// 効率的なクエリ例
func getRecentGames(userID string, limit int) ([]*Game, error) {
    // インデックスを活用したクエリ
    query := client.Collection("games").
        Where("userId", "==", userID).
        OrderBy("gameDate", firestore.Desc).
        Limit(limit)
    
    docs, err := query.Documents(ctx).GetAll()
    if err != nil {
        return nil, err
    }
    
    // バッチ読み取りで効率化
    var games []*Game
    for _, doc := range docs {
        var game Game
        if err := doc.DataTo(&game); err != nil {
            continue
        }
        games = append(games, &game)
    }
    
    return games, nil
}
```

## 10. 変更履歴

| バージョン | 日付 | 変更内容 | 担当者 |
|-----------|------|----------|--------|
| 2.0.0 | 2024-09-19 | Firebase Firestore版に移行、TTL機能追加 | システムエンジニア |

---

**注意事項**:
- 本設計書はFirebase Firestoreの特性を考慮した設計
- TTL機能により3ヶ月後の自動削除を実装
- 無料枠内での運用を前提としたコスト最適化
- Firestoreセキュリティルールによる適切なアクセス制御