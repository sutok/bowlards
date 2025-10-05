# Swagger UI でのAPI認証テストガイド

## 概要

BackendのSwagger UI (`http://localhost:18080/docs`) でAPIをテストする際、Firebase IDトークンが必要です。
このドキュメントでは、IDトークンを取得してSwagger UIで使用する方法を説明します。

## HTTPBearerトークンとは

- Firebase Authentication で発行されるIDトークン（JWT）
- ユーザー認証情報を含む署名付きトークン
- 有効期限は通常1時間

## トークン取得方法

### 方法1: ブラウザのDevToolsを使用（最も簡単）

1. **フロントエンドにログイン**
   - フロントエンド (`http://localhost:13000`) にアクセス
   - メールアドレスとパスワードでログイン

2. **ブラウザのDevToolsを開く**
   - Chrome/Edge: `F12` または `Cmd+Option+I` (Mac) / `Ctrl+Shift+I` (Windows)
   - Consoleタブを選択

3. **以下のコマンドを実行してトークンを取得**
   ```javascript
   import { auth } from './firebase/config';
   const user = auth.currentUser;
   if (user) {
     user.getIdToken().then(token => {
       console.log('Firebase ID Token:');
       console.log(token);
       // クリップボードにコピー
       navigator.clipboard.writeText(token);
       console.log('✅ トークンがクリップボードにコピーされました！');
     });
   } else {
     console.error('ログインしていません');
   }
   ```

4. **Swagger UIで使用**
   - `http://localhost:18080/docs` にアクセス
   - 右上の「Authorize」ボタンをクリック
   - `HTTPBearer (http, Bearer)` の入力欄にトークンを貼り付け
   - 「Authorize」をクリック

### 方法2: Pythonヘルパースクリプトを使用

1. **ヘルパースクリプトを実行**
   ```bash
   cd backend
   python scripts/get_firebase_token.py
   ```

2. **メールアドレスとパスワードを入力**
   - Firebaseに登録済みのアカウント情報を入力

3. **表示されたトークンをコピー**

4. **Swagger UIで使用**
   - 方法1と同様にAuthorizeボタンから認証

### 方法3: curlでトークンを取得（高度な方法）

Firebase Authentication REST APIを使用してトークンを取得：

```bash
# 環境変数を設定
export FIREBASE_API_KEY="your-firebase-api-key"
export USER_EMAIL="test@example.com"
export USER_PASSWORD="your-password"

# トークンを取得
curl -X POST "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key=${FIREBASE_API_KEY}" \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"${USER_EMAIL}\",\"password\":\"${USER_PASSWORD}\",\"returnSecureToken\":true}" | jq -r '.idToken'
```

## Swagger UIでの認証手順

1. **Swagger UIにアクセス**
   ```
   http://localhost:18080/docs
   ```

2. **Authorizeボタンをクリック**
   - ページ右上の緑色の「Authorize」ボタンをクリック

3. **トークンを入力**
   - `HTTPBearer (http, Bearer)` の入力欄に取得したトークンを貼り付け
   - ※ `Bearer` プレフィックスは不要（自動的に追加されます）

4. **Authorizeをクリック**
   - 認証が完了すると、錠前アイコンが閉じた状態になります

5. **APIをテスト**
   - 認証が必要なエンドポイントをテストできるようになります
   - 各エンドポイントの「Try it out」ボタンをクリック
   - パラメータを入力して「Execute」をクリック

## トークンの有効期限

- Firebase IDトークンは通常**1時間**有効です
- 有効期限が切れた場合、以下のエラーが表示されます：
  ```json
  {
    "detail": "Expired ID token"
  }
  ```
- 期限切れの場合は、新しいトークンを取得して再度認証してください

## トラブルシューティング

### エラー: "Invalid ID token"

**原因:**
- トークンが不正または破損している
- トークンの形式が間違っている

**解決方法:**
1. トークン全体がコピーされているか確認
2. 余分な空白や改行が含まれていないか確認
3. 新しいトークンを取得して再試行

### エラー: "Expired ID token"

**原因:**
- トークンの有効期限（1時間）が切れている

**解決方法:**
- 新しいトークンを取得して認証し直す

### エラー: "User not found"

**原因:**
- Firestoreにユーザー情報が登録されていない

**解決方法:**
1. フロントエンドから一度ログイン
2. または `/api/v1/users/me` エンドポイントを呼び出してユーザー登録

## テスト用アカウントの作成

開発環境でテスト用アカウントを作成するには：

1. **フロントエンドから作成**
   - `http://localhost:13000` にアクセス
   - 「新規登録」タブから作成

2. **Firebase Consoleから作成**
   - Firebase Console → Authentication → Users
   - 「Add user」からメールアドレスとパスワードを設定

## セキュリティに関する注意事項

⚠️ **重要:**
- IDトークンは機密情報です
- トークンを他人と共有しないでください
- ログやGitコミットにトークンを含めないでください
- 本番環境のトークンは特に慎重に扱ってください

## 関連ドキュメント

- [Firebase Authentication Design](./firebase-authentication-design.md)
- [Firebase Authentication Flow](./firebase-authentication-flow.md)
- [API Design](./api-design.md)

