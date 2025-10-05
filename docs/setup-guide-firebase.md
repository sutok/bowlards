# Firebaseデータ保存セットアップガイド（完全版）

## 📋 このガイドについて

このガイドでは、`.env.local`ファイルの設定からFirebaseへのデータ保存ができるまでの**全手順**を説明します。

**所要時間**: 約15-20分

## 🎯 ゴール

ゲーム終了時にFirebaseにデータが保存されることを確認する

---

## ステップ1: Firebase Consoleから情報を取得

### 1-1. Firebase Consoleにアクセス

1. ブラウザで以下のURLにアクセス
   ```
   https://console.firebase.google.com/
   ```

2. Googleアカウントでログイン

3. プロジェクト「**bowlards-dev**」を選択
   - プロジェクトが存在しない場合は、新規作成してください

### 1-2. Web API設定を取得

1. 左サイドバーの**⚙️ 歯車アイコン（プロジェクトの設定）**をクリック

2. 「**全般**」タブを選択

3. 下にスクロールして「**マイアプリ**」セクションを探す

4. ウェブアプリが登録されていない場合：
   - 「**アプリを追加**」をクリック
   - **</> ウェブ**アイコンを選択
   - アプリのニックネーム：`Bowlards Frontend`
   - 「**Firebase Hosting も設定する**」はチェックなし
   - 「**アプリを登録**」をクリック

5. 表示される設定情報をメモ帳にコピー
   ```javascript
   const firebaseConfig = {
     apiKey: "AIzaSyD1234567890abcdefghijklmnopqrstuvwxyz",
     authDomain: "bowlards-dev.firebaseapp.com",
     projectId: "bowlards-dev",
     storageBucket: "bowlards-dev.appspot.com",
     messagingSenderId: "123456789012",
     appId: "1:123456789012:web:abc123def456"
   };
   ```

**📝 メモ**: この情報は後で`.env.local`に転記します

### 1-3. Firebase Authenticationを有効化

1. 左サイドバーの「**Authentication**」をクリック

2. 「**始める**」をクリック（初めての場合）

3. 「**Sign-in method**」タブを選択

4. 「**Google**」を選択
   - 「有効にする」をONに切り替え
   - プロジェクトのサポートメール：自分のメールアドレス
   - 「**保存**」をクリック

5. 必要に応じて「**メール/パスワード**」も有効化

### 1-4. Cloud Firestoreを有効化

1. 左サイドバーの「**Firestore Database**」をクリック

2. 「**データベースの作成**」をクリック

3. ロケーションを選択
   - 推奨：`asia-northeast1 (Tokyo)`
   - 「**次へ**」をクリック

4. セキュリティルールを選択
   - **本番環境モード**を選択（後でルールを設定）
   - 「**作成**」をクリック

5. データベースの作成が完了するまで待つ（1-2分）

---

## ステップ2: Firestoreセキュリティルールを設定

### 2-1. セキュリティルールの設定

1. Firestore Databaseの画面で「**ルール**」タブをクリック

2. 以下のルールをコピー＆ペースト

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // ユーザーは自分のゲームデータのみアクセス可能
    match /games/{gameId} {
      allow read, write: if request.auth != null && request.auth.uid == resource.data.userId;
      allow create: if request.auth != null && request.auth.uid == request.resource.data.userId;
    }
    
    // ユーザーは自分のプロフィールのみアクセス可能
    match /users/{userId} {
      allow read, write: if request.auth != null && request.auth.uid == userId;
    }
  }
}
```

3. 「**公開**」をクリック

**📝 説明**: このルールにより、認証済みユーザーは自分のデータのみアクセスできます

---

## ステップ3: バックエンドAPIのURLを確認

### 3-1. ローカル開発環境の場合

バックエンドAPIのURL：
```
http://localhost:8000/api
```

### 3-2. 本番環境の場合

デプロイ済みのバックエンドAPIのURL（例）：
```
https://your-backend-api.run.app/api
```

**📝 メモ**: このURLは後で`.env.local`に転記します

---

## ステップ4: `.env.local`ファイルを作成

### 4-1. ターミナルを開く

```bash
# プロジェクトのルートディレクトリに移動
cd /Users/kazuh/Documents/GitHub/bowlards
```

### 4-2. サンプルファイルをコピー

```bash
# フロントエンド用の.env.localを作成
cp env.local.example .env.local
```

### 4-3. `.env.local`を編集

エディタで`.env.local`を開きます：

```bash
# VSCode の場合
code .env.local

# Cursor の場合
cursor .env.local

# vi の場合
vi .env.local
```

### 4-4. ステップ1で取得した情報を転記

**ステップ1-2で取得したFirebase設定を転記**:

```bash
# フロントエンド用Firebase設定
VITE_FIREBASE_API_KEY=AIzaSyD1234567890abcdefghijklmnopqrstuvwxyz
VITE_FIREBASE_AUTH_DOMAIN=bowlards-dev.firebaseapp.com
VITE_FIREBASE_PROJECT_ID=bowlards-dev
VITE_FIREBASE_STORAGE_BUCKET=bowlards-dev.appspot.com
VITE_FIREBASE_MESSAGING_SENDER_ID=123456789012
VITE_FIREBASE_APP_ID=1:123456789012:web:abc123def456

# バックエンドAPI設定
VITE_API_BASE_URL=http://localhost:8000/api
```

**⚠️ 重要**: 
- `VITE_FIREBASE_API_KEY`: ステップ1-2の`apiKey`の値
- `VITE_FIREBASE_AUTH_DOMAIN`: ステップ1-2の`authDomain`の値
- `VITE_FIREBASE_PROJECT_ID`: ステップ1-2の`projectId`の値
- `VITE_FIREBASE_STORAGE_BUCKET`: ステップ1-2の`storageBucket`の値
- `VITE_FIREBASE_MESSAGING_SENDER_ID`: ステップ1-2の`messagingSenderId`の値
- `VITE_FIREBASE_APP_ID`: ステップ1-2の`appId`の値
- `VITE_API_BASE_URL`: ステップ3で確認したURL

### 4-5. ファイルを保存

- VSCode/Cursor: `Cmd + S` (Mac) または `Ctrl + S` (Windows)
- vi: `Esc` → `:wq` → `Enter`

---

## ステップ5: バックエンドの設定（Admin SDK用）

### 5-1. サービスアカウントキーを取得

1. Firebase Console > **プロジェクトの設定** > **サービスアカウント**タブ

2. 下にスクロールして「**新しい秘密鍵の生成**」をクリック

3. 「**キーを生成**」をクリック

4. JSONファイルがダウンロードされる（例：`bowlards-dev-abc123.json`）

### 5-2. JSONファイルを配置

```bash
# ダウンロードフォルダからcredentialsフォルダに移動
mv ~/Downloads/bowlards-dev-*.json /Users/kazuh/Documents/GitHub/bowlards/credentials/

# ファイル名を確認
ls -la /Users/kazuh/Documents/GitHub/bowlards/credentials/
```

**出力例**:
```
-rw-------  1 kazuh  staff  2365 Oct  4 10:30 bowlards-dev-877e4635f23c.json
```

### 5-3. ファイル権限を設定（セキュリティ対策）

```bash
chmod 600 /Users/kazuh/Documents/GitHub/bowlards/credentials/bowlards-dev-*.json
```

### 5-4. バックエンドの`.env`を設定

```bash
# バックエンドディレクトリに移動
cd /Users/kazuh/Documents/GitHub/bowlards/backend

# サンプルファイルをコピー
cp env.example .env

# .envを編集
code .env  # または cursor .env
```

以下の内容を追加/編集:

```bash
# Firebase設定
APP_FIREBASE_PROJECT_ID=bowlards-dev
APP_FIREBASE_CREDENTIALS_PATH=../credentials/bowlards-dev-877e4635f23c.json

# サーバー設定
APP_HOST=0.0.0.0
APP_PORT=8000
APP_DEBUG=true
```

**⚠️ 重要**: `APP_FIREBASE_CREDENTIALS_PATH`のファイル名は、実際にダウンロードしたファイル名に合わせてください

---

## ステップ6: アプリケーションを起動

### 6-1. バックエンドを起動

```bash
# バックエンドディレクトリで実行
cd /Users/kazuh/Documents/GitHub/bowlards/backend

# 依存関係をインストール（初回のみ）
pip install -r requirements.txt
# または
uv sync

# サーバーを起動
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**成功メッセージ**を確認:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [12345]
INFO:     Started server process [12346]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### 6-2. フロントエンドを起動

**新しいターミナルウィンドウ**を開いて実行:

```bash
# フロントエンドディレクトリに移動
cd /Users/kazuh/Documents/GitHub/bowlards/frontend

# 依存関係をインストール（初回のみ）
npm install

# 開発サーバーを起動
npm run dev
```

**成功メッセージ**を確認:
```
  VITE v4.x.x  ready in 500 ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
  ➜  press h to show help
```

---

## ステップ7: 動作確認

### 7-1. ブラウザでアクセス

```
http://localhost:5173/
```

### 7-2. Googleアカウントでログイン

1. 「**ログイン**」ボタンをクリック
2. Googleアカウントを選択
3. 認証を許可

### 7-3. ゲームを記録

1. ダッシュボードから「**ゲーム記録**」をクリック

2. 各フレームのスコアを入力
   - テストなので適当な値でOK（例：全部5本ずつ）

3. 全10フレーム入力完了後、「**ゲーム終了**」ボタンをクリック

4. **保存中...**の表示を確認

5. **成功ダイアログ**が表示されることを確認
   ```
   ゲーム完了
   お疲れ様でした！
   最終スコア: XX点
   ゲームデータがFirebaseに保存されました
   ```

### 7-4. Firebase Consoleでデータを確認

1. Firebase Console > **Firestore Database**を開く

2. 左側のコレクション一覧で「**games**」をクリック

3. 保存されたゲームドキュメントが表示されることを確認

**確認項目**:
- ✅ ドキュメントIDが存在する
- ✅ `userId`フィールドに自分のUIDが入っている
- ✅ `totalScore`フィールドにスコアが入っている
- ✅ `frames`フィールドに10個のフレームデータが入っている
- ✅ `status`フィールドが`"completed"`になっている
- ✅ `gameDate`フィールドにタイムスタンプが入っている

---

## ✅ 成功チェックリスト

すべて✅になればセットアップ完了です！

### 環境設定
- [ ] `.env.local`ファイルが作成されている
- [ ] Firebase設定（6項目）がすべて正しく入力されている
- [ ] `VITE_API_BASE_URL`が設定されている
- [ ] バックエンドの`.env`ファイルが設定されている
- [ ] サービスアカウントキーが配置されている

### Firebase設定
- [ ] Firebase Authenticationが有効化されている
- [ ] Google認証が有効化されている
- [ ] Cloud Firestoreが作成されている
- [ ] セキュリティルールが設定されている

### アプリケーション
- [ ] バックエンドが起動している（http://localhost:8000）
- [ ] フロントエンドが起動している（http://localhost:5173）
- [ ] Googleでログインできる
- [ ] ゲームを記録できる
- [ ] ゲーム終了ボタンをクリックできる
- [ ] 「保存中...」表示が出る
- [ ] 成功ダイアログが表示される
- [ ] Firebase Consoleでデータが確認できる

---

## 🔧 トラブルシューティング

### 問題1: 「Firebase: Error (auth/invalid-api-key)」

**原因**: `VITE_FIREBASE_API_KEY`が間違っている

**解決方法**:
1. Firebase Console > プロジェクト設定 > 全般 で`apiKey`を再確認
2. `.env.local`の`VITE_FIREBASE_API_KEY`を修正
3. フロントエンドを再起動（`Ctrl+C` → `npm run dev`）
4. ブラウザのキャッシュをクリア（`Cmd+Shift+R`）

### 問題2: 「Network Error」が表示される

**原因**: バックエンドAPIに接続できない

**解決方法**:
1. バックエンドが起動しているか確認
   ```bash
   curl http://localhost:8000/api/health
   # または
   curl http://localhost:8000/
   ```
2. `.env.local`の`VITE_API_BASE_URL`を確認
3. フロントエンドを再起動

### 問題3: 「Permission denied」エラー

**原因**: Firestoreセキュリティルールが設定されていない

**解決方法**:
1. Firebase Console > Firestore Database > ルール
2. ステップ2-1のルールを再設定
3. 「公開」をクリック
4. アプリをリロード

### 問題4: ログインできない

**原因**: Firebase Authenticationが有効化されていない

**解決方法**:
1. Firebase Console > Authentication
2. Sign-in method > Google を有効化
3. サポートメールアドレスを設定
4. 保存

### 問題5: バックエンドが起動しない

**原因**: サービスアカウントキーが読み込めない

**解決方法**:
```bash
# 1. ファイルが存在するか確認
ls -la credentials/

# 2. .envのパスを確認
cat backend/.env | grep CREDENTIALS_PATH

# 3. パスが正しいか確認（backend/.envから見た相対パス）
cat ../credentials/bowlards-dev-*.json

# 4. 必要に応じて絶対パスに変更
APP_FIREBASE_CREDENTIALS_PATH=/Users/kazuh/Documents/GitHub/bowlards/credentials/bowlards-dev-xxx.json
```

### 問題6: 環境変数が読み込まれない

**解決方法**:
1. ファイル名を確認（`.env.local`であること）
2. プロジェクトのルートディレクトリにあることを確認
3. 開発サーバーを再起動
4. ブラウザのキャッシュをクリア

---

## 📞 サポート

問題が解決しない場合は、以下の情報とともに開発チームに連絡してください：

1. エラーメッセージのスクリーンショット
2. ブラウザのコンソールログ
3. バックエンドのログ
4. `.env.local`の内容（APIキーは伏せて）

**コンソールログの確認方法**:
- Chrome: `Cmd+Option+J` (Mac) / `Ctrl+Shift+J` (Windows)
- ブラウザの「Console」タブを確認

---

## 📚 関連ドキュメント

- [環境変数設定ガイド](./environment-variables-guide.md)
- [Firebase認証フロー完全ガイド](./firebase-authentication-flow.md)
- [ゲーム保存機能実装ガイド](./game-save-implementation.md)

---

## 🎉 おめでとうございます！

すべてのステップが完了し、Firebaseにデータが保存されることを確認できました！

次のステップ：
- ゲーム履歴画面の実装
- ユーザープロフィール画面の実装
- 統計情報の表示

---

**最終更新**: 2025年10月4日

