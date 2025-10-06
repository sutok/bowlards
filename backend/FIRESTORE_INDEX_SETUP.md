# Firestoreインデックス設定手順

## 問題

`/api/v1/games/history` エンドポイントでゲーム履歴を取得する際、以下のエラーが発生：

```
400 The query requires an index.
```

このエラーは、Firestoreで `user_id` でフィルタリングし、`played_at` でソートするクエリを実行する際に複合インデックスが必要なため発生します。

## 解決方法

### 方法1: Firebase Consoleから手動で作成（推奨・最速）

1. エラーログに記載されたURLにアクセス：
   ```
   https://console.firebase.google.com/v1/r/project/bowlards-dev/firestore/indexes?create_composite=...
   ```

2. 「インデックスを作成」ボタンをクリック

3. インデックスが作成されるまで数分待つ（通常1-5分）

4. `/api/v1/games/history` エンドポイントを再度テスト

### 方法2: Firebase CLIで自動デプロイ

#### 前提条件
```bash
npm install -g firebase-tools
firebase login
```

#### インデックスのデプロイ
```bash
cd /Users/kazuh/Documents/GitHub/bowlards/backend
firebase deploy --only firestore:indexes --project bowlards-dev
```

#### デプロイ確認
```bash
firebase firestore:indexes --project bowlards-dev
```

## 作成されるインデックス

### インデックス1: 基本的な履歴取得
- **コレクション**: `games`
- **フィールド**:
  - `user_id` (ASCENDING)
  - `played_at` (DESCENDING)
- **用途**: ユーザーごとの全ゲーム履歴を新しい順に取得

### インデックス2: ステータスフィルター付き履歴取得
- **コレクション**: `games`
- **フィールド**:
  - `user_id` (ASCENDING)
  - `status` (ASCENDING)
  - `played_at` (DESCENDING)
- **用途**: ユーザーごとの特定ステータス（completed, in_progress等）のゲーム履歴を新しい順に取得

## 動作確認

インデックス作成後、以下のエンドポイントをテスト：

```bash
# 全ゲーム履歴
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "https://your-api.com/api/v1/games/history?limit=20&offset=0"

# completedステータスのみ
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "https://your-api.com/api/v1/games/history?limit=20&offset=0&status=completed"
```

## トラブルシューティング

### インデックス作成が失敗する場合

1. Firebase Consoleでプロジェクトが正しく選択されているか確認
2. Firestoreが有効化されているか確認
3. 適切な権限があるか確認（Editor以上）

### インデックスが反映されない場合

- インデックス作成には数分かかります
- Firebase Consoleの「Firestore Database」→「インデックス」タブで状態を確認
- ステータスが「作成中」から「有効」になるまで待つ

## 参考

- [Firestore インデックスの管理](https://firebase.google.com/docs/firestore/query-data/indexing)
- [複合インデックスのベストプラクティス](https://firebase.google.com/docs/firestore/query-data/index-overview)
