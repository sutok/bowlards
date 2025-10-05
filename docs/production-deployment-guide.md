# Firebase本番環境への切り替えガイド

## 概要

このガイドでは、Firebaseエミュレータから本番環境への切り替えに必要な変更点を説明します。

## 必要な変更点

### 1. フロントエンドの変更

#### 1.1 Firebase設定の変更

**現在の設定（エミュレータ）:**
```typescript
// frontend/src/firebase/config.ts
const firebaseConfig = {
  apiKey: "demo-key",
  authDomain: "bowlards-dev.firebaseapp.com",
  projectId: "bowlards-dev",
  // ...
};

// エミュレータに接続
if (import.meta.env.DEV) {
  connectAuthEmulator(auth, `http://${authEmulatorHost}:${authEmulatorPort}`);
  connectFirestoreEmulator(db, firestoreEmulatorHost, parseInt(firestoreEmulatorPort));
}
```

**本番環境への変更:**
```typescript
// frontend/src/firebase/config.production.ts
const firebaseConfig = {
  apiKey: import.meta.env.VITE_FIREBASE_API_KEY,
  authDomain: import.meta.env.VITE_FIREBASE_AUTH_DOMAIN,
  projectId: import.meta.env.VITE_FIREBASE_PROJECT_ID,
  storageBucket: import.meta.env.VITE_FIREBASE_STORAGE_BUCKET,
  messagingSenderId: import.meta.env.VITE_FIREBASE_MESSAGING_SENDER_ID,
  appId: import.meta.env.VITE_FIREBASE_APP_ID
};

// エミュレータ接続を削除
export const auth = getAuth(app);
export const db = getFirestore(app);
```

#### 1.2 環境変数の設定

```bash
# .env.production
VITE_FIREBASE_API_KEY=your-production-api-key
VITE_FIREBASE_AUTH_DOMAIN=your-project.firebaseapp.com
VITE_FIREBASE_PROJECT_ID=your-production-project-id
VITE_FIREBASE_STORAGE_BUCKET=your-project.appspot.com
VITE_FIREBASE_MESSAGING_SENDER_ID=your-sender-id
VITE_FIREBASE_APP_ID=your-app-id
```

### 2. バックエンドの変更

#### 2.1 Firebase認証の変更

**現在の設定（エミュレータ）:**
```python
# backend/app/auth/firebase.py
# エミュレータ環境変数を使用
FIREBASE_AUTH_EMULATOR_HOST=firebase-emulator
FIREBASE_AUTH_EMULATOR_PORT=9099
```

**本番環境への変更:**
```python
# backend/app/auth/firebase.production.py
# 本番環境用認証情報を使用
if settings.firebase_credentials_path:
    cred = credentials.Certificate(settings.firebase_credentials_path)
    firebase_admin.initialize_app(cred)
```

#### 2.2 環境変数の設定

```bash
# .env.production
APP_FIREBASE_PROJECT_ID=your-production-project-id
APP_FIREBASE_CREDENTIALS_PATH=/path/to/service-account-key.json
# または
APP_FIREBASE_PRIVATE_KEY=your-private-key
APP_FIREBASE_CLIENT_EMAIL=your-client-email
```

### 3. Docker Composeの変更

#### 3.1 エミュレータサービスの削除

**現在の設定:**
```yaml
# docker-compose.yml
services:
  firebase-emulator:
    # Firebaseエミュレータ設定
```

**本番環境:**
```yaml
# docker-compose.production.yml
services:
  # firebase-emulatorサービスを削除
  frontend:
    environment:
      - VITE_FIREBASE_API_KEY=${VITE_FIREBASE_API_KEY}
      # 本番環境用Firebase設定
  backend:
    environment:
      - APP_FIREBASE_PROJECT_ID=${APP_FIREBASE_PROJECT_ID}
      # 本番環境用Firebase設定
```

## 本番環境へのデプロイ手順

### 1. Firebaseプロジェクトの準備

1. **Firebase Console**でプロジェクトを作成
2. **Authentication**を有効化
3. **Firestore Database**を作成
4. **サービスアカウントキー**を生成

### 2. 環境変数の設定

```bash
# 本番環境用環境変数ファイルを作成
cp env.production.example .env.production

# 実際の値に置き換え
vim .env.production
```

### 3. サービスアカウントキーの配置

```bash
# サービスアカウントキーを配置
mkdir -p credentials
cp your-service-account-key.json credentials/
```

### 4. 本番環境での起動

```bash
# 本番環境用Docker Composeで起動
docker-compose -f docker-compose.production.yml up -d
```

## セキュリティ考慮事項

### 1. 環境変数の管理

- 本番環境の環境変数は安全に管理
- サービスアカウントキーは適切に保護
- シークレット管理サービス（AWS Secrets Manager等）の使用を推奨

### 2. Firebase Security Rules

```javascript
// Firestore Security Rules
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /{document=**} {
      allow read, write: if request.auth != null;
    }
  }
}
```

### 3. CORS設定

```python
# 本番環境用CORS設定
allowed_origins = [
    "https://your-domain.com",
    "https://www.your-domain.com"
]
```

## トラブルシューティング

### 1. 認証エラー

- サービスアカウントキーの権限を確認
- Firebaseプロジェクトの設定を確認
- 環境変数の設定を確認

### 2. 接続エラー

- ネットワーク設定を確認
- ファイアウォール設定を確認
- DNS設定を確認

### 3. パフォーマンス問題

- Firebaseの料金プランを確認
- クエリの最適化
- インデックスの設定

## 監視とログ

### 1. ログ設定

```python
# 本番環境用ログ設定
APP_LOG_LEVEL=INFO
APP_LOG_FORMAT=json
```

### 2. 監視設定

- Firebase Consoleでの監視
- アプリケーションログの監視
- パフォーマンス監視

## まとめ

本番環境への切り替えでは以下の点に注意してください：

1. **Firebase設定の変更**: エミュレータ設定を削除し、本番環境用設定に変更
2. **認証情報の設定**: サービスアカウントキーまたは環境変数で認証情報を設定
3. **セキュリティの強化**: 適切なSecurity RulesとCORS設定
4. **監視の設定**: ログとパフォーマンスの監視設定

これらの変更により、Firebaseエミュレータから本番環境への安全な切り替えが可能になります。
