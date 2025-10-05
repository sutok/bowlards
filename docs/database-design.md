# データベース設計書（Firebase Firestore版）

## 1. 概要

### 1.1 データベース名
scoring-bawlards

### 1.2 設計の目的
ボーリングスコア記録・管理アプリケーションのFirebase Firestoreデータベース設計。ユーザー情報、ゲーム記録、統計情報を効率的に管理し、TTL（Time To Live）による自動データ削除を実装する。

### 1.3 対象システム
- **データベース**: Firebase Firestore
- **認証**: Firebase Authentication
- **ストレージ**: Firebase Storage（プロフィール画像用）
- **ホスティング**: Firebase Hosting

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
```javascript
// コレクション: users
// ドキュメントID: Firebase UID
{
  "email": "user@example.com",
  "displayName": "ユーザー名",
  "photoURL": "https://example.com/photo.jpg",
  "createdAt": "2024-01-01T00:00:00Z",
  "updatedAt": "2024-01-01T00:00:00Z",
  "lastLoginAt": "2024-01-01T00:00:00Z"
}
```

#### 3.1.2 セキュリティルール
```javascript
// Firestore Security Rules
match /users/{userId} {
  allow read, write: if request.auth != null && request.auth.uid == userId;
}
```

### 3.2 ゲームコレクション (games)

#### 3.2.1 ドキュメント構造
```javascript
// コレクション: games
// ドキュメントID: 自動生成UUID
{
  "userId": "firebase_uid",
  "gameDate": "2024-01-01T00:00:00Z",
  "totalScore": 150,
  "status": "completed", // "in_progress" | "completed"
  "frames": [
    {
      "frameNumber": 1,
      "firstRoll": 7,
      "secondRoll": 3,
      "thirdRoll": null,
      "frameScore": 10,
      "isStrike": false,
      "isSpare": true,
      "isCompleted": true
    }
    // ... 10フレーム分
  ],
  "statistics": {
    "strikeCount": 2,
    "spareCount": 3,
    "averageScore": 150.0
  },
  "createdAt": "2024-01-01T00:00:00Z",
  "updatedAt": "2024-01-01T00:00:00Z",
  "expireAt": "2024-04-01T00:00:00Z" // TTL用（3ヶ月後）
}
```

#### 3.2.2 セキュリティルール
```javascript
match /games/{gameId} {
  allow read, write: if request.auth != null && 
    request.auth.uid == resource.data.userId;
  allow create: if request.auth != null && 
    request.auth.uid == request.resource.data.userId;
}
```

### 3.3 ユーザー統計コレクション (userStatistics)

#### 3.3.1 ドキュメント構造
```javascript
// コレクション: userStatistics
// ドキュメントID: Firebase UID
{
  "userId": "firebase_uid",
  "totalGames": 25,
  "averageScore": 145.5,
  "highestScore": 200,
  "lowestScore": 80,
  "totalStrikes": 15,
  "totalSpares": 30,
  "gamesThisMonth": 8,
  "lastUpdated": "2024-01-01T00:00:00Z",
  "createdAt": "2024-01-01T00:00:00Z"
}
```

## 4. TTL（Time To Live）設定

### 4.1 TTLポリシー設定
```javascript
// Firebase Console または Admin SDK で設定
const ttlPolicy = {
  collection: 'games',
  field: 'expireAt',
  ttl: 90 // 90日（3ヶ月）
};
```

### 4.2 データ作成時のTTL設定
```javascript
// ゲーム作成時のTTL設定例
const gameData = {
  userId: user.uid,
  gameDate: new Date(),
  totalScore: 0,
  status: 'in_progress',
  frames: [],
  createdAt: new Date(),
  updatedAt: new Date(),
  expireAt: new Date(Date.now() + 90 * 24 * 60 * 60 * 1000) // 90日後
};
```

## 5. インデックス設計

### 5.1 複合インデックス
```javascript
// Firestore Console で設定
// コレクション: games
// フィールド: userId (昇順), gameDate (降順)
// 用途: ユーザー別ゲーム履歴取得

// コレクション: games  
// フィールド: userId (昇順), status (昇順)
// 用途: ユーザー別進行中ゲーム取得
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

## 7. コスト最適化

### 7.1 無料枠内での運用
```javascript
// 月間想定使用量（100ユーザー、500ゲーム）
const monthlyUsage = {
  storage: '0.5GB', // 無料枠: 1GB
  reads: '10,000',  // 無料枠: 50,000
  writes: '8,000',  // 無料枠: 20,000
  deletes: '6,000'  // 無料枠: 20,000
};
```

## 8. 変更履歴

| バージョン | 日付 | 変更内容 | 担当者 |
|-----------|------|----------|--------|
| 2.0.0 | 2024-09-19 | Firebase Firestore版に移行、TTL機能追加 | システムエンジニア |

---

**注意事項**:
- 本設計書はFirebase Firestoreの特性を考慮した設計
- TTL機能により3ヶ月後の自動削除を実装
- 無料枠内での運用を前提としたコスト最適化
- セキュリティルールによる適切なアクセス制御
