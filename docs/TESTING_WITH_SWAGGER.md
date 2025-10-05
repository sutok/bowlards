# Swagger UIでのAPIテストガイド（クイックリファレンス）

## 🎯 目的

BackendのSwagger UI (`http://localhost:18080/docs`) で認証が必要なAPIをテストする方法

## 🔑 HTTPBearerトークンとは？

Swagger UIの「Authorize」ボタンで要求される**Firebase IDトークン**です。

- Firebase Authenticationで発行されるJWT（JSON Web Token）
- ユーザーの認証情報を含む
- 有効期限: 約1時間

## ⚡ 最も簡単な取得方法（推奨）

### ステップ1: フロントエンドでログイン

```
http://localhost:13000
```

メールアドレスとパスワードでログイン

### ステップ2: ブラウザコンソールでトークン取得

1. **DevToolsを開く**
   - Windows/Linux: `F12` または `Ctrl + Shift + I`
   - Mac: `Cmd + Option + I`

2. **Consoleタブを選択**

3. **以下をコピー＆ペーストして実行**

```javascript
auth.currentUser.getIdToken().then(token => {
  console.log('🔑 Firebase ID Token:');
  console.log(token);
  navigator.clipboard.writeText(token);
  console.log('✅ クリップボードにコピーしました！');
});
```

### ステップ3: Swagger UIで認証

1. **Swagger UIを開く**
   ```
   http://localhost:18080/docs
   ```

2. **Authorizeボタンをクリック**
   - ページ右上の緑色のボタン

3. **トークンを貼り付け**
   - `HTTPBearer (http, Bearer)` の入力欄に `Cmd+V` / `Ctrl+V`
   - ※ `Bearer` という文字は**入力不要**（自動で追加されます）

4. **Authorizeをクリック**

5. **🎉 完了！**
   - 錠前アイコンが閉じた状態になれば成功
   - 認証が必要なAPIをテストできます

## 📝 ブラウザコンソールスニペット（詳細版）

より詳しい情報が必要な場合は、以下のスニペットを使用：

```javascript
// docs/browser-console-snippet.js の内容を使用
```

または、ファイルから直接コピー：
```bash
cat docs/browser-console-snippet.js
```

## 🐍 Pythonスクリプトで取得

ブラウザを使わずにトークンを取得したい場合：

```bash
cd backend
python scripts/get_firebase_token.py
```

メールアドレスとパスワードを入力するだけでトークンが取得できます。

## 🔄 トークンの有効期限

- **有効期限**: 約1時間
- **期限切れエラー**: 
  ```json
  {
    "detail": "Expired ID token"
  }
  ```
- **対処法**: 新しいトークンを取得して再度Authorize

## 💡 トラブルシューティング

### ❌ エラー: "Invalid ID token"

**チェック項目:**
- [ ] トークン全体がコピーされているか
- [ ] 余分な空白や改行が含まれていないか
- [ ] ログイン状態が有効か

**解決方法:**
新しいトークンを取得して再試行

### ❌ エラー: "auth is not defined" (ブラウザコンソール)

**原因:**
Firebase authオブジェクトがグローバルに公開されていない

**解決方法:**

```javascript
// Reactアプリケーション内で実行する場合
import { auth } from './firebase/config';
const token = await auth.currentUser.getIdToken();
console.log(token);
```

または、React DevToolsのComponentsタブから認証状態を確認

### ❌ エラー: "User not found"

**原因:**
Firestoreにユーザー情報が未登録

**解決方法:**
1. フロントエンドから一度ログイン
2. または `/api/v1/users/me` エンドポイントを呼び出し

## 📚 関連ドキュメント

- [詳細なSwagger Testing Guide](./swagger-testing-guide.md)
- [Firebase Authentication Design](./firebase-authentication-design.md)
- [Firebase Authentication Flow](./firebase-authentication-flow.md)
- [API Design](./api-design.md)

## 🔐 セキュリティ上の注意

⚠️ **IDトークンは機密情報です**

- ❌ トークンを他人と共有しない
- ❌ ログやGitコミットにトークンを含めない
- ❌ 公開チャットやフォーラムに貼り付けない
- ✅ 本番環境のトークンは特に慎重に扱う

## 🎓 学習リソース

### Firebase IDトークンの構造

IDトークンはJWT形式で、3つの部分から構成されます：

```
header.payload.signature
```

- **header**: トークンのメタデータ
- **payload**: ユーザー情報（uid, email, exp等）
- **signature**: トークンの検証用署名

### トークンのデコード（確認用）

```javascript
// ブラウザコンソールで実行
const token = 'your-token-here';
const payload = JSON.parse(atob(token.split('.')[1]));
console.log(payload);
```

出力例：
```json
{
  "uid": "abc123...",
  "email": "user@example.com",
  "iat": 1234567890,
  "exp": 1234571490
}
```

---

**更新日**: 2025-10-05

