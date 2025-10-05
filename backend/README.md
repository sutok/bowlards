# Scoring Bowlards Backend (FastAPI)

ボーリングスコア記録・管理アプリケーションのFastAPIバックエンドAPIサーバーです。

## 機能

- ユーザー管理（Firebase認証連携）
- ボーリングゲーム記録・管理
- スコア計算（ストライク・スペア対応）
- ゲーム履歴・統計情報
- リアルタイムAPI

## 技術スタック

- **フレームワーク**: FastAPI 0.104+
- **言語**: Python 3.13+
- **データベース**: Google Cloud Firestore
- **認証**: Firebase Authentication
- **ASGIサーバー**: Uvicorn

## セットアップ

### 1. uvのインストール

```bash
# uvをインストール（推奨）
curl -LsSf https://astral.sh/uv/install.sh | sh

# または pipでインストール
pip install uv
```

### 2. 依存関係のインストール

```bash
# 本番用依存関係
uv pip install -e .

# 開発用依存関係
uv pip install -e ".[dev]"

# または Makefileを使用
make install-dev
```

### 2. 環境変数の設定

```bash
# 環境変数ファイルをコピー
cp env.example .env

# .envファイルを編集
# Firebase設定、データベース設定などを入力
```

### 3. Firebase設定

Firebase認証情報を設定してください：

```bash
# 方法1: サービスアカウントキーファイル
APP_FIREBASE_CREDENTIALS_PATH=./credentials.json

# 方法2: 環境変数
APP_FIREBASE_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n"
APP_FIREBASE_CLIENT_EMAIL=your-service-account@your-project.iam.gserviceaccount.com
```

### 4. アプリケーション起動

```bash
# 開発環境
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 本番環境
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000

# または Makefileを使用
make run
```

## Dockerでの実行

```bash
# 開発環境
docker-compose up -d

# ログ確認
docker-compose logs -f backend

# 停止
docker-compose down
```

## API仕様

### Swagger UIでのテスト

Swagger UIで認証が必要なAPIをテストするには、Firebase IDトークンが必要です。

#### クイックスタート（ブラウザコンソールで取得）

1. フロントエンド (http://localhost:13000) にログイン
2. ブラウザのDevToolsを開く（F12）
3. Consoleタブで以下を実行：

```javascript
auth.currentUser.getIdToken().then(token => {
  console.log('Token:', token);
  navigator.clipboard.writeText(token);
  console.log('✅ コピーしました！');
});
```

4. Swagger UI (http://localhost:18080/docs) で「Authorize」ボタンをクリック
5. トークンを貼り付けて「Authorize」

詳しくは [Swagger Testing Guide](../docs/swagger-testing-guide.md) を参照してください。

#### Pythonスクリプトで取得

```bash
python scripts/get_firebase_token.py
```

### エンドポイント

| メソッド | エンドポイント | 説明 | 認証 |
|---------|---------------|------|------|
| GET | `/` | ヘルスチェック | 不要 |
| GET | `/health` | ヘルスチェック | 不要 |
| GET | `/docs` | Swagger UI | 不要 |
| GET | `/api/v1/users/profile` | ユーザープロフィール取得 | 必要 |
| PUT | `/api/v1/users/profile` | ユーザープロフィール更新 | 必要 |
| DELETE | `/api/v1/users/profile` | ユーザー削除 | 必要 |
| POST | `/api/v1/games` | ゲーム作成 | 必要 |
| GET | `/api/v1/games/{id}` | ゲーム取得 | 必要 |
| POST | `/api/v1/games/{id}/roll` | ロール追加 | 必要 |
| DELETE | `/api/v1/games/{id}` | ゲーム削除 | 必要 |
| GET | `/api/v1/games/history` | ゲーム履歴取得 | 必要 |
| GET | `/api/v1/games/statistics` | ゲーム統計取得 | 必要 |

### 認証

Firebase JWTトークンを使用：

```http
Authorization: Bearer <Firebase_JWT_Token>
```

### レスポンス形式

#### 成功レスポンス
```json
{
  "success": true,
  "data": {
    // レスポンスデータ
  },
  "meta": {
    "total": 100,
    "limit": 20,
    "offset": 0
  }
}
```

#### エラーレスポンス
```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Error message"
  }
}
```

## テスト

```bash
# 全テスト実行
uv run pytest

# カバレッジ付きテスト
uv run pytest --cov=app

# 特定のテストファイル実行
uv run pytest tests/test_main.py

# または Makefileを使用
make test
make test-cov
```

## 開発

### コード品質

```bash
# コードフォーマット
uv run black app/

# インポート整理
uv run isort app/

# リント
uv run flake8 app/

# 型チェック
uv run mypy app/

# または Makefileを使用
make format
make lint
```

### プレコミットフック

```bash
# プレコミットフック設定
uv run pre-commit install

# 手動実行
uv run pre-commit run --all-files
```

## デプロイ

### Google Cloud Run

```bash
# イメージビルド
docker build -t gcr.io/PROJECT_ID/bowlards-backend .

# イメージプッシュ
docker push gcr.io/PROJECT_ID/bowlards-backend

# Cloud Runデプロイ
gcloud run deploy bowlards-backend \
  --image gcr.io/PROJECT_ID/bowlards-backend \
  --platform managed \
  --region asia-northeast1 \
  --allow-unauthenticated
```

## 監視・ログ

### ログレベル

- `ERROR`: エラー情報
- `WARN`: 警告情報
- `INFO`: 一般的な情報
- `DEBUG`: デバッグ情報

### メトリクス

- `/metrics` エンドポイントでPrometheusメトリクスを提供

## ライセンス

MIT License
