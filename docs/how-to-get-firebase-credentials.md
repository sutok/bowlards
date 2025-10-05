# Firebase認証情報の取得方法（完全ガイド）

## 概要

このガイドでは、バックエンド用のFirebase認証情報を取得する方法を説明します。

## 取得する情報

バックエンド（Python/Go）でFirebase Admin SDKを使用する際に必要な認証情報：

| 環境変数名 | 説明 | 例 |
|----------|------|-----|
| `APP_FIREBASE_PROJECT_ID` | FirebaseプロジェクトID | `project_id` |
| `APP_FIREBASE_PRIVATE_KEY` | サービスアカウントの秘密鍵 | `-----BEGIN PRIVATE KEY-----\n...` |
| `APP_FIREBASE_CLIENT_EMAIL` | サービスアカウントのメールアドレス | `firebase-adminsdk-xxxxx@your-project.iam.gserviceaccount.com` |

---

## 方法1: サービスアカウントキー（JSONファイル）から取得【推奨】

### ステップ1: Firebase Consoleにアクセス

1. ブラウザで以下のURLにアクセス
   ```
   https://console.firebase.google.com/
   ```

2. Googleアカウントでログイン

3. プロジェクト「**project_id**」を選択

### ステップ2: サービスアカウントキーをダウンロード

1. 左サイドバーの **⚙️ 歯車アイコン（プロジェクトの設定）** をクリック

2. 上部タブの **「サービスアカウント」** をクリック

3. ページ中央の説明文を確認
   ```
   Firebase Admin SDK
   Firebase Admin SDK を使用すると、バックエンドサーバーから Firebase にアクセスできます。
   ```

4. 下にスクロールして **「新しい秘密鍵の生成」** ボタンをクリック

5. 確認ダイアログが表示される
   ```
   新しい秘密鍵を生成しますか？
   この鍵により、プロジェクトの Firebase サービスへの管理者アクセス権が付与されます。
   ```

6. **「キーを生成」** ボタンをクリック

7. JSONファイルが自動的にダウンロードされる
   - ファイル名例: `project_id-877e4635f23c.json`
   - ダウンロード先: 通常は`~/Downloads/`フォルダ

### ステップ3: JSONファイルの中身を確認


### ステップ4: 必要な情報を抽出

| JSONのキー | 環境変数名 | 値の例 |
|-----------|----------|-------|
| `project_id` | `APP_FIREBASE_PROJECT_ID` | `project_id` |
| `private_key` | `APP_FIREBASE_PRIVATE_KEY` | `-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n` |
| `client_email` | `APP_FIREBASE_CLIENT_EMAIL` | `firebase-adminsdk-fbsvc@project_id.iam.gserviceaccount.com` |

---

## 方法2: ターミナルで自動抽出【便利】

既にJSONファイルをダウンロード済みの場合、以下のコマンドで自動的に値を抽出できます。

### macOS/Linux の場合

```bash
# プロジェクトルートに移動
cd /Users/kazuh/Documents/GitHub/bowlards

# JSONファイルのパスを確認
ls -la credentials/

# project_id を抽出
cat credentials/project_id-*.json | grep -o '"project_id": "[^"]*"' | cut -d'"' -f4

# client_email を抽出
cat credentials/project_id-*.json | grep -o '"client_email": "[^"]*"' | cut -d'"' -f4

# private_key を抽出（改行コードを含む）
cat credentials/project_id-*.json | grep -o '"private_key": "[^"]*"' | cut -d'"' -f4
```

### jqコマンドを使用する場合（より正確）

```bash
# jqがインストールされていない場合
brew install jq  # macOS
# または
sudo apt-get install jq  # Linux

# project_id を抽出
jq -r '.project_id' credentials/project_id-*.json

# client_email を抽出
jq -r '.client_email' credentials/project_id-*.json

# private_key を抽出
jq -r '.private_key' credentials/project_id-*.json
```

**出力例**:
```bash
# project_id
project_id

# client_email
firebase-adminsdk-fbsvc@project_id.iam.gserviceaccount.com

# private_key
-----BEGIN PRIVATE KEY-----
MIIEvwIBADANBgkqhkiG9w0BAQEFAASCBKkwggSlAgEAAoIBAQCoG//h9DkPS4PO
...
-----END PRIVATE KEY-----
```

---

## 方法3: Firebase Consoleで直接確認

**注意**: Firebase Consoleでは、一度生成した秘密鍵を再表示することは**できません**。

### 既存のサービスアカウントを確認

1. Firebase Console > プロジェクトの設定 > サービスアカウント

2. 「サービスアカウントの管理」リンクをクリック
   - Google Cloud Console のIAMページに移動

3. サービスアカウント一覧で以下を確認:
   - **メールアドレス**: `client_email`に対応
     ```
     firebase-adminsdk-fbsvc@project_id.iam.gserviceaccount.com
     ```
   - **秘密鍵**: ここでは表示されない（再生成が必要）

### プロジェクトIDを確認

1. Firebase Console > プロジェクトの設定 > 全般タブ

2. 「プロジェクトID」欄を確認
   ```
   project_id
   ```

---

## 設定方法の比較

### A. JSONファイルを使用する方法【開発環境推奨】

**メリット**:
- 設定が簡単
- すべての情報が1つのファイルに含まれている
- ローカル開発に最適

**デメリット**:
- ファイルの管理が必要
- 本番環境には不向き

**設定例**:
```bash
# backend/.env
APP_FIREBASE_CREDENTIALS_PATH=../credentials/project_id-877e4635f23c.json
```

**コード例（Python）**:
```python
from firebase_admin import credentials, initialize_app
import os

cred_path = os.getenv('APP_FIREBASE_CREDENTIALS_PATH')
cred = credentials.Certificate(cred_path)
initialize_app(cred)
```

### B. 環境変数を使用する方法【本番環境推奨】

**メリット**:
- ファイル管理不要
- 本番環境に最適
- Secret Manager等と連携可能

**デメリット**:
- 設定が少し複雑
- 改行コードの扱いに注意が必要

**設定例**:
```bash
# backend/.env（本番環境）
APP_FIREBASE_PROJECT_ID=project_id
APP_FIREBASE_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\nMIIEvwIBADANBgkqhkiG9w0BAQEFAASCBKkwggSlAgEAAo...\n-----END PRIVATE KEY-----\n"
APP_FIREBASE_CLIENT_EMAIL=firebase-adminsdk-fbsvc@project_id.iam.gserviceaccount.com
```

**コード例（Python）**:
```python
from firebase_admin import credentials, initialize_app
import os

cred = credentials.Certificate({
    'type': 'service_account',
    'project_id': os.getenv('APP_FIREBASE_PROJECT_ID'),
    'private_key': os.getenv('APP_FIREBASE_PRIVATE_KEY'),
    'client_email': os.getenv('APP_FIREBASE_CLIENT_EMAIL'),
})
initialize_app(cred)
```

---

## 実践例：JSONファイルから環境変数へ変換

### ステップ1: JSONファイルから値を取得

```bash
cd /Users/kazuh/Documents/GitHub/bowlards

# 値を変数に格納
PROJECT_ID=$(jq -r '.project_id' credentials/project_id-*.json)
CLIENT_EMAIL=$(jq -r '.client_email' credentials/project_id-*.json)
PRIVATE_KEY=$(jq -r '.private_key' credentials/project_id-*.json)

# 確認
echo "PROJECT_ID: $PROJECT_ID"
echo "CLIENT_EMAIL: $CLIENT_EMAIL"
echo "PRIVATE_KEY: (秘密鍵のため表示省略)"
```

### ステップ2: .envファイルに追記

```bash
# backend/.envに追記（本番環境用）
cat >> backend/.env << EOF

# Firebase認証情報（環境変数方式）
APP_FIREBASE_PROJECT_ID=${PROJECT_ID}
APP_FIREBASE_CLIENT_EMAIL=${CLIENT_EMAIL}
APP_FIREBASE_PRIVATE_KEY="${PRIVATE_KEY}"
EOF
```

### ステップ3: 動作確認

```bash
# バックエンドを起動して確認
cd backend
uvicorn app.main:app --reload
```

---

## 注意事項とベストプラクティス

### 🔒 セキュリティ

1. **秘密鍵は絶対に公開しない**
   - Gitにコミットしない（`.gitignore`に追加）
   - 公開リポジトリに含めない
   - スクリーンショットに含めない

2. **ファイル権限を設定**
   ```bash
   chmod 600 credentials/*.json
   ```

3. **定期的なローテーション**
   - 本番環境では定期的に鍵を再生成
   - 古い鍵は無効化

### 📁 ファイル管理

```
bowlards/
├── credentials/
│   ├── project_id-877e4635f23c.json  # 開発環境用（Git除外）
│   ├── bowlards-prod-xxx.json          # 本番環境用（Git除外）
│   └── README.md                       # 説明ファイル（Git管理）
├── backend/
│   ├── .env                            # 環境変数（Git除外）
│   └── env.example                     # サンプル（Git管理）
└── .gitignore                          # 除外設定
```

### ✅ .gitignoreの設定

```bash
# .gitignore に以下を追加
credentials/*.json
!credentials/README.md
backend/.env
.env
.env.local
.env.production
```

---

## トラブルシューティング

### 問題1: 「秘密鍵をダウンロードしたが見つからない」

**解決方法**:
```bash
# Downloadsフォルダを確認
ls -la ~/Downloads/bowlards-*.json

# 見つかったら移動
mv ~/Downloads/project_id-*.json /Users/kazuh/Documents/GitHub/bowlards/credentials/
```

### 問題2: 「private_keyに改行コードが含まれる」

**解決方法**:

改行コード`\n`は**そのまま**文字列として扱います：

```bash
# 正しい形式
APP_FIREBASE_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\nMIIEvwIBADA...\n-----END PRIVATE KEY-----\n"

# ❌ 間違い（実際の改行を入れない）
APP_FIREBASE_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----
MIIEvwIBADA...
-----END PRIVATE KEY-----"
```

### 問題3: 「Could not load the default credentials」

**原因**: 認証情報が正しく読み込まれていない

**解決方法**:
```bash
# 1. ファイルが存在するか確認
ls -la credentials/project_id-*.json

# 2. JSONの構文が正しいか確認
cat credentials/project_id-*.json | jq .

# 3. 環境変数が設定されているか確認（開発環境）
cat backend/.env | grep CREDENTIALS_PATH

# 4. バックエンドを再起動
cd backend
uvicorn app.main:app --reload
```

---

## まとめ

### 取得方法

| 情報 | Firebase Console での場所 |
|-----|-------------------------|
| `APP_FIREBASE_PROJECT_ID` | プロジェクト設定 > 全般 > プロジェクトID |
| `APP_FIREBASE_PRIVATE_KEY` | プロジェクト設定 > サービスアカウント > 新しい秘密鍵の生成 → JSONファイル内の`private_key` |
| `APP_FIREBASE_CLIENT_EMAIL` | プロジェクト設定 > サービスアカウント > 新しい秘密鍵の生成 → JSONファイル内の`client_email` |

### クイックリファレンス

```bash
# JSONファイルから値を抽出
cd /Users/kazuh/Documents/GitHub/bowlards

# プロジェクトID
jq -r '.project_id' credentials/project_id-*.json

# クライアントメール
jq -r '.client_email' credentials/project_id-*.json

# 秘密鍵（注意：機密情報）
jq -r '.private_key' credentials/project_id-*.json
```

### 次のステップ

1. ✅ サービスアカウントキーをダウンロード
2. ✅ `credentials/`フォルダに配置
3. ✅ 必要に応じて環境変数を設定
4. ✅ バックエンドの`.env`を更新
5. ✅ アプリケーションをテスト

---

## 参考リンク

- [Firebase Admin SDK セットアップ](https://firebase.google.com/docs/admin/setup)
- [サービスアカウントについて](https://cloud.google.com/iam/docs/service-accounts)
- [環境変数のベストプラクティス](https://12factor.net/config)

---

**最終更新**: 2025年10月4日

