# 環境変数設定ガイド

## 1. 概要

このドキュメントでは、Bowlardsアプリケーションで使用される環境変数について説明します。

## 2. 環境変数の種類

### 2.1 フロントエンド環境変数（VITE_*）

#### 2.1.1 `VITE_FIREBASE_API_KEY`
**用途**: フロントエンド用のFirebase Web APIキー

**説明**:
- Firebaseプロジェクトの公開APIキー
- フロントエンド（ブラウザ）からFirebaseサービスにアクセスするために使用
- Firebase Console > プロジェクト設定 > 全般 > ウェブアプリから取得
- **公開情報のため、コミットしても問題ない**（ただし、Firebase Security Rulesで保護が必要）

**重要**: このキーは公開されることを前提としており、悪用を防ぐためにFirebaseのセキュリティルールで保護します。

**取得方法**:
```
1. Firebase Console (https://console.firebase.google.com) にアクセス
2. プロジェクトを選択
3. プロジェクト設定（歯車アイコン）をクリック
4. 「全般」タブを選択
5. 「マイアプリ」セクションで「ウェブアプリ」を選択
6. 「apiKey」の値をコピー
```

**例**:
```bash
VITE_FIREBASE_API_KEY=AIzaSyD1234567890abcdefghijklmnopqrstuvwxyz
```

#### 2.1.2 `VITE_API_BASE_URL`
**用途**: バックエンドAPIのベースURL

**説明**:
- フロントエンドがバックエンドAPIにアクセスするためのURL
- 環境ごとに異なる値を設定

**例**:
```bash
# ローカル開発環境
VITE_API_BASE_URL=http://localhost:8000/api

# 本番環境
VITE_API_BASE_URL=https://api.your-domain.com/api
```

### 2.2 バックエンド環境変数（APP_*）

#### 2.2.1 `SECRET_KEY` または `APP_SECRET_KEY`
**用途**: バックエンドアプリケーションの秘密鍵

**説明**:
- バックエンドで使用される秘密鍵
- セッション管理、JWT署名、データ暗号化などに使用
- **絶対に公開してはいけない**
- **Gitにコミットしてはいけない**
- ランダムな長い文字列を使用すべき

**生成方法**:
```bash
# Pythonの場合
python -c "import secrets; print(secrets.token_urlsafe(32))"

# OpenSSLの場合
openssl rand -base64 32

# Node.jsの場合
node -e "console.log(require('crypto').randomBytes(32).toString('base64'))"
```

**例**:
```bash
SECRET_KEY=a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6
```

#### 2.2.2 `APP_FIREBASE_PROJECT_ID`
**用途**: FirebaseプロジェクトID

**説明**:
- バックエンドがFirebase Admin SDKを使用する際に必要
- Firebase Console > プロジェクト設定で確認可能

**例**:
```bash
APP_FIREBASE_PROJECT_ID=bowlards-dev
```

#### 2.2.3 `APP_FIREBASE_CREDENTIALS_PATH`
**用途**: Firebase Admin SDK認証情報ファイルのパス

**説明**:
- サービスアカウントキーのJSONファイルへのパス
- **このファイルは絶対に公開してはいけない**
- Firebase Console > プロジェクト設定 > サービスアカウント から生成

**例**:
```bash
APP_FIREBASE_CREDENTIALS_PATH=./credentials/bowlards-dev-service-account.json
```

## 3. 環境変数の比較表

| 環境変数 | 用途 | 使用場所 | 公開可否 | 重要度 |
|---------|------|---------|---------|--------|
| `VITE_FIREBASE_API_KEY` | Firebase Web API | フロントエンド | ✅ 公開可（Security Rulesで保護） | 中 |
| `SECRET_KEY` | アプリの秘密鍵 | バックエンド | ❌ 絶対に非公開 | 高 |
| `APP_FIREBASE_PROJECT_ID` | FirebaseプロジェクトID | バックエンド | ✅ 公開可 | 低 |
| `APP_FIREBASE_CREDENTIALS_PATH` | サービスアカウントキー | バックエンド | ❌ 絶対に非公開 | 高 |
| `VITE_API_BASE_URL` | バックエンドURL | フロントエンド | ✅ 公開可 | 低 |

## 4. よくある質問（FAQ）

### Q1: `VITE_FIREBASE_API_KEY`と`SECRET_KEY`は同じものですか？

**A**: **いいえ、全く別のものです。**

- **`VITE_FIREBASE_API_KEY`**: Firebaseが提供する公開APIキーで、フロントエンドからFirebaseサービスにアクセスするために使用します。このキーは公開されることを前提としており、Firebase Security Rulesで保護します。

- **`SECRET_KEY`**: バックエンドアプリケーションが内部で使用する秘密鍵で、セッション管理やトークンの署名などに使用します。このキーは**絶対に公開してはいけません**。

### Q2: `VITE_FIREBASE_API_KEY`は公開しても大丈夫ですか？

**A**: **はい、大丈夫です。** ただし、以下の条件を満たす必要があります：

1. Firebase Security Rulesを適切に設定
2. Firebase Authentication Rulesを設定
3. APIキーの使用制限を設定（Firebase Console > 認証情報）

Firebase Web APIキーは、ブラウザで実行されるJavaScriptコードに含まれるため、必然的に公開されます。悪用を防ぐためには、Security Rulesで適切にアクセス制御を行います。

### Q3: 環境変数ファイルはGitにコミットすべきですか？

**A**: 以下のルールに従ってください：

| ファイル | コミット |
|---------|---------|
| `.env` | ❌ NO（.gitignoreに追加） |
| `.env.local` | ❌ NO（.gitignoreに追加） |
| `.env.production` | ❌ NO（.gitignoreに追加） |
| `env.example` | ✅ YES（サンプルとして） |
| `env.local.example` | ✅ YES（サンプルとして） |
| `env.production.example` | ✅ YES（サンプルとして） |

### Q4: 本番環境でも同じ環境変数を使えますか？

**A**: **いいえ、環境ごとに異なる値を設定してください。**

特に以下の変数は必ず環境ごとに変更してください：
- `SECRET_KEY`（本番環境では強力なランダム文字列を使用）
- `VITE_API_BASE_URL`（本番環境のURLを指定）
- `APP_FIREBASE_PROJECT_ID`（本番用のFirebaseプロジェクトを使用）
- `APP_DEBUG`（本番環境では`false`に設定）

## 5. セキュリティベストプラクティス

### 5.1 秘密情報の管理

✅ **推奨**:
- `.env`ファイルは`.gitignore`に追加
- 秘密情報は環境変数または秘密管理サービス（GCP Secret Manager等）で管理
- 本番環境の`SECRET_KEY`は長くランダムな文字列を使用
- 定期的にシークレットキーをローテーション

❌ **非推奨**:
- 秘密情報をコードに直接記述
- `.env`ファイルをGitにコミット
- 開発環境と本番環境で同じシークレットキーを使用
- 簡単に推測できる文字列をシークレットキーに使用

### 5.2 Firebase APIキーの保護

Firebase Web APIキーは公開されますが、以下の対策で保護します：

1. **Firebase Security Rules**
```javascript
// Firestoreのセキュリティルール例
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // ユーザーは自分のゲームデータのみアクセス可能
    match /games/{gameId} {
      allow read, write: if request.auth != null && request.auth.uid == resource.data.userId;
    }
    
    // ユーザーは自分のプロフィールのみアクセス可能
    match /users/{userId} {
      allow read, write: if request.auth != null && request.auth.uid == userId;
    }
  }
}
```

2. **APIキーの使用制限**
- Firebase Console > 認証情報 > APIキーを制限
- アプリケーションの制限を設定（HTTPリファラーなど）

## 6. 環境変数の設定手順

### 6.1 ローカル開発環境

```bash
# 1. サンプルファイルをコピー
cp env.local.example .env.local

# 2. .env.localファイルを編集
# フロントエンド用の環境変数を設定
VITE_FIREBASE_API_KEY=your-actual-firebase-api-key
VITE_FIREBASE_AUTH_DOMAIN=your-project.firebaseapp.com
VITE_FIREBASE_PROJECT_ID=bowlards-dev
VITE_FIREBASE_STORAGE_BUCKET=your-project.appspot.com
VITE_FIREBASE_MESSAGING_SENDER_ID=123456789
VITE_FIREBASE_APP_ID=1:123456789:web:abc123
VITE_API_BASE_URL=http://localhost:8000/api

# 3. バックエンド用の環境変数を設定
cd backend
cp env.example .env

# 4. backend/.envファイルを編集
SECRET_KEY=your-generated-secret-key-here
APP_FIREBASE_PROJECT_ID=bowlards-dev
APP_FIREBASE_CREDENTIALS_PATH=./credentials/bowlards-dev-service-account.json
```

### 6.2 本番環境

本番環境では、環境変数を直接サーバーに設定するか、GCP Secret Managerなどの秘密管理サービスを使用します。

```bash
# GCP Cloud Runの場合
gcloud run deploy bowlards-backend \
  --set-env-vars="SECRET_KEY=${SECRET_KEY}" \
  --set-env-vars="APP_FIREBASE_PROJECT_ID=${FIREBASE_PROJECT_ID}"

# Docker Composeの場合
docker-compose --env-file .env.production up -d
```

## 7. トラブルシューティング

### 問題: Firebase認証エラー

**症状**: 「Permission denied」エラーが表示される

**解決方法**:
1. `VITE_FIREBASE_API_KEY`が正しいか確認
2. Firebase Security Rulesが適切に設定されているか確認
3. ユーザーが認証済みか確認

### 問題: バックエンドAPIに接続できない

**症状**: 「Network Error」が表示される

**解決方法**:
1. `VITE_API_BASE_URL`が正しいか確認
2. バックエンドサーバーが起動しているか確認
3. CORS設定が適切か確認

### 問題: 環境変数が反映されない

**症状**: 環境変数の値が変更されない

**解決方法**:
1. Viteの場合、開発サーバーを再起動
2. ブラウザのキャッシュをクリア
3. `.env`ファイルの命名規則が正しいか確認（`.env.local`など）

## 8. 参考資料

- [Firebase Web API Key について](https://firebase.google.com/docs/projects/api-keys)
- [Vite 環境変数](https://vitejs.dev/guide/env-and-mode.html)
- [Firebase Security Rules](https://firebase.google.com/docs/firestore/security/get-started)

## 9. 変更履歴

| バージョン | 日付 | 変更内容 | 担当者 |
|----------|------|----------|--------|
| 1.0.0 | 2025-10-04 | 初版作成 | システムエンジニア |

---

**重要な注意事項**:
- このドキュメントを読んでも不明な点がある場合は、開発チームに相談してください
- 秘密情報は絶対に公開リポジトリにコミットしないでください
- 本番環境の設定を変更する前に、必ずバックアップを取ってください

