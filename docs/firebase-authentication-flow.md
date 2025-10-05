# Firebase認証フロー完全ガイド

## 1. 概要

Bowlardsアプリケーションでは、**2種類のFirebase認証**を使用しています：
1. **フロントエンド用**: Firebase Web API（環境変数から設定）
2. **バックエンド用**: Firebase Admin SDK（サービスアカウントキーファイル）

## 2. 認証の種類と設定方法

### 2.1 フロントエンド用Firebase認証

#### 使用場所
- React フロントエンド
- ブラウザで実行されるJavaScript

#### 設定方法
**環境変数ファイル（`.env.local`）に記述**:

```bash
# .env.local
VITE_FIREBASE_API_KEY=AIzaSyD1234567890abcdefghijklmnopqrstuvwxyz
VITE_FIREBASE_AUTH_DOMAIN=bowlards-dev.firebaseapp.com
VITE_FIREBASE_PROJECT_ID=bowlards-dev
VITE_FIREBASE_STORAGE_BUCKET=bowlards-dev.appspot.com
VITE_FIREBASE_MESSAGING_SENDER_ID=123456789
VITE_FIREBASE_APP_ID=1:123456789:web:abc123
```

#### コードでの読み込み
```typescript
// frontend/src/firebase/config.ts
import { initializeApp } from 'firebase/app';

const firebaseConfig = {
  apiKey: import.meta.env.VITE_FIREBASE_API_KEY,
  authDomain: import.meta.env.VITE_FIREBASE_AUTH_DOMAIN,
  projectId: import.meta.env.VITE_FIREBASE_PROJECT_ID,
  // ...
};

const app = initializeApp(firebaseConfig);
```

#### 取得方法
Firebase Console > プロジェクト設定 > 全般 > マイアプリ

---

### 2.2 バックエンド用Firebase認証（Admin SDK）

#### 使用場所
- Python/Go バックエンド
- サーバーサイドで実行

#### 設定方法A: サービスアカウントキーファイル（開発環境）

**JSONファイル**: `credentials/bowlards-dev-877e4635f23c.json`

```json
{
  "type": "service_account",
  "project_id": "bowlards-dev",
  "private_key_id": "877e46...",
  "private_key": "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-fbsvc@bowlards-dev.iam.gserviceaccount.com",
  "client_id": "103686950184386533331",
  // ...
}
```

**環境変数でパスを指定**:
```bash
# backend/.env
APP_FIREBASE_CREDENTIALS_PATH=./credentials/bowlards-dev-877e4635f23c.json
```

**コードでの読み込み（Python）**:
```python
# backend/app/auth/firebase.py
import os
from google.cloud import firestore
from firebase_admin import credentials, initialize_app

cred_path = os.getenv('APP_FIREBASE_CREDENTIALS_PATH')
cred = credentials.Certificate(cred_path)
initialize_app(cred)

db = firestore.Client()
```

#### 設定方法B: 環境変数（本番環境推奨）

```bash
# backend/.env (本番環境)
APP_FIREBASE_PROJECT_ID=bowlards-dev
APP_FIREBASE_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n"
APP_FIREBASE_CLIENT_EMAIL=firebase-adminsdk-fbsvc@bowlards-dev.iam.gserviceaccount.com
```

**コードでの読み込み（Python）**:
```python
import os
from firebase_admin import credentials, initialize_app

cred = credentials.Certificate({
    'type': 'service_account',
    'project_id': os.getenv('APP_FIREBASE_PROJECT_ID'),
    'private_key': os.getenv('APP_FIREBASE_PRIVATE_KEY'),
    'client_email': os.getenv('APP_FIREBASE_CLIENT_EMAIL'),
})
initialize_app(cred)
```

#### 取得方法
Firebase Console > プロジェクト設定 > サービスアカウント > 新しい秘密鍵の生成

---

## 3. 認証フロー図

```mermaid
graph TB
    subgraph Frontend["フロントエンド（ブラウザ）"]
        A[React App] -->|読み込み| B[.env.local]
        B -->|環境変数| C[firebase/config.ts]
        C -->|初期化| D[Firebase Web SDK]
    end
    
    subgraph Backend["バックエンド（サーバー）"]
        E[Python/Go App] -->|読み込み| F[.env または JSONファイル]
        F -->|認証情報| G[Firebase Admin SDK]
    end
    
    D -->|Web API| H[Firebase Services]
    G -->|Admin API| H
    
    H -->|認証/DB操作| I[(Firestore)]
    
    style B fill:#e1f5ff
    style F fill:#ffe1e1
    style H fill:#fff4e1
```

## 4. ファイルと環境変数の対応表

| ファイル/環境変数 | 用途 | 読み込み先 | 公開可否 |
|-----------------|------|-----------|---------|
| `.env.local` | フロントエンド設定 | React App | ✅ 一部公開可 |
| `VITE_FIREBASE_API_KEY` | Firebase Web API | フロントエンド | ✅ 公開可（Security Rulesで保護） |
| `credentials/*.json` | バックエンド認証 | Python/Go App | ❌ 絶対に非公開 |
| `APP_FIREBASE_CREDENTIALS_PATH` | JSONファイルパス | バックエンド | ⚠️ パスのみ |
| `APP_FIREBASE_PRIVATE_KEY` | 秘密鍵（本番） | バックエンド | ❌ 絶対に非公開 |

## 5. よくある誤解

### ❌ 誤解1: 「firebase.json」から認証情報を読み込む

**正解**: `firebase.json`は**Firebase CLIの設定ファイル**で、認証情報とは関係ありません。

```json
// firebase.json（もし存在すれば）
{
  "hosting": {
    "public": "dist",
    "ignore": ["firebase.json"]
  }
}
```

これはデプロイ設定などに使用され、認証情報は含まれません。

### ❌ 誤解2: フロントエンドとバックエンドで同じ認証方法

**正解**: それぞれ**異なる認証方法**を使用します。

| | フロントエンド | バックエンド |
|---|-------------|------------|
| **SDK** | Firebase Web SDK | Firebase Admin SDK |
| **認証方法** | Web API Key | Service Account |
| **設定場所** | `.env.local` | `.env` + JSONファイル |
| **権限** | ユーザーレベル | 管理者レベル |

### ❌ 誤解3: サービスアカウントキーは環境変数だけで完結

**正解**: 2つの方法があります。

1. **開発環境**: JSONファイル（簡単）
   ```bash
   APP_FIREBASE_CREDENTIALS_PATH=./credentials/bowlards-dev.json
   ```

2. **本番環境**: 環境変数（安全）
   ```bash
   APP_FIREBASE_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\n..."
   APP_FIREBASE_CLIENT_EMAIL="..."
   ```

## 6. 設定の流れ（ステップバイステップ）

### 6.1 フロントエンド設定

```bash
# 1. Firebase Consoleから設定を取得
# Firebase Console > プロジェクト設定 > 全般 > マイアプリ

# 2. .env.localファイルを作成
cp env.local.example .env.local

# 3. Firebase設定を記入
cat > .env.local << EOF
VITE_FIREBASE_API_KEY=AIzaSyD1234567890abcdefghijklmnopqrstuvwxyz
VITE_FIREBASE_AUTH_DOMAIN=bowlards-dev.firebaseapp.com
VITE_FIREBASE_PROJECT_ID=bowlards-dev
VITE_FIREBASE_STORAGE_BUCKET=bowlards-dev.appspot.com
VITE_FIREBASE_MESSAGING_SENDER_ID=123456789
VITE_FIREBASE_APP_ID=1:123456789:web:abc123
VITE_API_BASE_URL=http://localhost:8000/api
EOF

# 4. フロントエンド起動
cd frontend
npm run dev
```

### 6.2 バックエンド設定（開発環境）

```bash
# 1. サービスアカウントキーを取得
# Firebase Console > プロジェクト設定 > サービスアカウント > 
# 新しい秘密鍵の生成 > JSONをダウンロード

# 2. JSONファイルを配置
mv ~/Downloads/bowlards-dev-*.json credentials/bowlards-dev.json

# 3. ファイル権限を設定
chmod 600 credentials/bowlards-dev.json

# 4. .envファイルを作成
cd backend
cp env.example .env

# 5. 認証情報パスを記入
cat >> .env << EOF
APP_FIREBASE_PROJECT_ID=bowlards-dev
APP_FIREBASE_CREDENTIALS_PATH=../credentials/bowlards-dev.json
EOF

# 6. バックエンド起動
uvicorn app.main:app --reload
```

### 6.3 バックエンド設定（本番環境）

```bash
# 1. サービスアカウントキーから値を抽出
cat credentials/bowlards-dev.json | jq -r '.private_key'
cat credentials/bowlards-dev.json | jq -r '.client_email'

# 2. 環境変数として設定（GCP Secret Managerなど）
gcloud secrets create firebase-private-key --data-file=<(jq -r '.private_key' credentials/bowlards-dev.json)

# 3. Cloud Runにデプロイ
gcloud run deploy bowlards-backend \
  --set-env-vars="APP_FIREBASE_PROJECT_ID=bowlards-dev" \
  --set-secrets="APP_FIREBASE_PRIVATE_KEY=firebase-private-key:latest"
```

## 7. 実際のファイル構成

```
bowlards/
├── frontend/
│   ├── .env.local                    # フロントエンド設定（作成が必要）
│   └── src/
│       └── firebase/
│           └── config.ts             # 環境変数を読み込む
│
├── backend/
│   ├── .env                          # バックエンド設定（作成が必要）
│   └── app/
│       └── auth/
│           └── firebase.py           # JSONファイルまたは環境変数を読み込む
│
├── credentials/
│   ├── bowlards-dev-877e4635f23c.json  # サービスアカウントキー
│   └── README.md                      # このディレクトリの説明
│
├── env.local.example                  # フロントエンド設定のサンプル
├── backend/env.example                # バックエンド設定のサンプル
└── .gitignore                         # 機密ファイルを除外
```

## 8. セキュリティチェックリスト

### フロントエンド
- [ ] `.env.local`は`.gitignore`に含まれている
- [ ] `VITE_FIREBASE_API_KEY`はFirebase Security Rulesで保護されている
- [ ] API使用制限が設定されている（Firebase Console）

### バックエンド
- [ ] `credentials/*.json`は`.gitignore`に含まれている
- [ ] JSONファイルの権限が`600`に設定されている
- [ ] 本番環境では環境変数を使用している
- [ ] サービスアカウントの権限が最小限に設定されている

### 共通
- [ ] `.env`ファイルはGitにコミットされていない
- [ ] サンプルファイル（`*.example`）のみコミットされている
- [ ] 機密情報は絶対に公開リポジトリに含まれていない

## 9. トラブルシューティング

### 問題: 「Could not load the default credentials」

**原因**: バックエンドがFirebaseサービスアカウントキーを読み込めない

**解決方法**:
```bash
# 1. ファイルが存在するか確認
ls -la credentials/

# 2. パスが正しいか確認
cat backend/.env | grep CREDENTIALS_PATH

# 3. 権限を確認
ls -l credentials/bowlards-dev-*.json

# 4. 必要に応じて権限を修正
chmod 600 credentials/bowlards-dev-*.json
```

### 問題: フロントエンドで「Firebase: Error (auth/invalid-api-key)」

**原因**: `VITE_FIREBASE_API_KEY`が正しく設定されていない

**解決方法**:
```bash
# 1. .env.localファイルが存在するか確認
ls -la frontend/.env.local

# 2. 環境変数が読み込まれているか確認（開発サーバーを再起動）
cd frontend
npm run dev

# 3. ブラウザコンソールで確認
# Firebase Consoleの設定と一致しているか確認
```

### 問題: 環境変数が反映されない

**解決方法**:
1. **Viteを再起動**: `npm run dev`を停止して再起動
2. **ブラウザキャッシュをクリア**: Ctrl+Shift+R（強制リロード）
3. **ファイル名を確認**: `.env.local`（先頭にドット）

## 10. まとめ

| 項目 | フロントエンド | バックエンド |
|-----|-------------|------------|
| **設定ファイル** | `.env.local` | `.env` + JSONファイル |
| **環境変数の接頭辞** | `VITE_` | `APP_` |
| **Firebase SDK** | Web SDK | Admin SDK |
| **認証情報** | Web API Key | Service Account |
| **権限レベル** | ユーザー | 管理者 |
| **公開可否** | 一部公開可 | 絶対非公開 |

**重要**: 
- `firebase.json`（Firebase CLI設定）と`credentials/*.json`（サービスアカウントキー）は全く別物です
- フロントエンドとバックエンドで異なる認証方法を使用します
- サービスアカウントキーは絶対に公開してはいけません

## 11. 参考リンク

- [Firebase Web SDK セットアップ](https://firebase.google.com/docs/web/setup)
- [Firebase Admin SDK セットアップ](https://firebase.google.com/docs/admin/setup)
- [サービスアカウント管理](https://cloud.google.com/iam/docs/service-accounts)

---

**変更履歴**

| バージョン | 日付 | 変更内容 |
|----------|------|----------|
| 1.0.0 | 2025-10-04 | 初版作成 |

