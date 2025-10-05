# Scoring Bawlards/Bowling

ボーリングスコア記録・管理アプリケーション

## 概要

Scoring Bawlards/Bowlingは、ユーザーがボーリングゲームのスコアを記録・管理できるWebアプリケーションです。

## 主な機能

- **ゲーム記録**: ボーリングゲームのスコアをリアルタイムで記録
- **自動スコア計算**: ストライク・スペアを含むボーリングルールに基づく自動計算
- **ゲーム保存**: 完了したゲームをFirebase Firestoreに自動保存
- **ゲーム履歴**: 過去のゲーム記録の閲覧と管理
- **ユーザー認証**: Firebase Authenticationによる安全なユーザー管理
- **統計情報**: ユーザーのボーリング統計データの表示

## 技術スタック

### フロントエンド
- React 18.x
- TypeScript
- Redux Toolkit
- Material-UI (MUI) v5
- Vite

### バックエンド
- Go 1.21+
- Echo v4
- GORM v2
- MySQL 8.0

### 認証
- Firebase Authentication

### インフラ
- Docker & Docker Compose
- Firebase Emulator

## 開発環境構築

### 前提条件
- Docker & Docker Compose
- Node.js 18.x+
- Go 1.21+
- Firebase CLI

### セットアップ手順

**📘 詳細な手順は [Firebaseセットアップガイド](docs/setup-guide-firebase.md) をご覧ください**

#### クイックスタート

1. **リポジトリクローン**
```bash
git clone <repository-url>
cd bowlards
```

2. **環境変数設定**
```bash
# ローカル開発環境用
cp env.local.example .env.local

# 本番環境用
cp env.production.example .env.production
```

3. **Firebase設定を転記**

`.env.local`を編集し、Firebase Consoleから取得した情報を設定：
```bash
VITE_FIREBASE_API_KEY=your-api-key-here
VITE_FIREBASE_AUTH_DOMAIN=your-project.firebaseapp.com
VITE_FIREBASE_PROJECT_ID=your-project-id
VITE_FIREBASE_STORAGE_BUCKET=your-project.appspot.com
VITE_FIREBASE_MESSAGING_SENDER_ID=your-sender-id
VITE_FIREBASE_APP_ID=your-app-id
VITE_API_BASE_URL=http://localhost:8000/api
```

**🔗 詳しい取得方法**: [Firebaseセットアップガイド](docs/setup-guide-firebase.md)

3. **Firebase CLIインストール**
```bash
npm install -g firebase-tools
```

4. **Firebaseログイン**
```bash
firebase login
```

5. **開発環境起動**
```bash
make dev-build
```

6. **データベースマイグレーション**
```bash
make db-migrate
```

7. **テストデータ投入**
```bash
make db-seed
```

### アクセスURL

- **フロントエンド**: http://localhost:3000
- **バックエンドAPI**: http://localhost:8080/api/v1
- **Nginx**: http://localhost:80
- **Firebase Auth Emulator**: http://localhost:9099
- **Firebase Emulator UI**: http://localhost:4000

## 開発コマンド

### 基本操作
```bash
# 開発環境起動
make dev

# 開発環境再ビルド
make dev-build

# 開発環境停止
make dev-down

# ログ確認
make dev-logs

# 開発環境クリーンアップ
make dev-clean
```

### データベース操作
```bash
# マイグレーション実行
make db-migrate

# テストデータ投入
make db-seed
```

### テスト実行
```bash
# バックエンドテスト
make test

# フロントエンドテスト
make test-frontend
```

### リント実行
```bash
# バックエンドリント
make lint-backend

# フロントエンドリント
make lint-frontend
```

## プロジェクト構造

```
bowlards/
├── docs/                    # 設計書
├── docker/                  # Docker設定
│   ├── nginx/              # Nginx設定
│   ├── mysql/              # MySQL初期化スクリプト
│   └── firebase/           # Firebase設定
├── frontend/               # Reactフロントエンド
├── backend/                # Goバックエンド
├── docker-compose.yml      # Docker Compose設定
├── Makefile               # 開発用コマンド
└── README.md              # このファイル
```

## 設計書

### 全体設計
- [フロントエンド全体設計書](docs/frontend-overall-design.md)
- [バックエンド全体設計書](docs/backend-overall-design.md)
- [データベース設計書](docs/database-design.md)
- [API設計書](docs/api-design.md)
- [画面設計書](docs/screen-design.md)
- [UI/UX設計書](docs/ui-ux-design.md)
- [Firebase認証設計書](docs/firebase-authentication-design.md)
- [開発環境構築設計書](docs/development-environment-design.md)

### 機能別設計
- [ゲーム記録作成機能設計書](docs/game-record-creation-design.md)
- [ゲーム保存機能実装ガイド](docs/game-save-implementation.md) ⭐ NEW
- [ゲーム履歴機能設計書](docs/game-history-design.md)
- [スコア計算設計書](docs/scoring.md)

### セットアップガイド
- [🔥 Firebaseセットアップガイド（完全版）](docs/setup-guide-firebase.md) ⭐ NEW
- [環境変数設定ガイド](docs/environment-variables-guide.md) ⭐ NEW
- [Firebase認証フロー完全ガイド](docs/firebase-authentication-flow.md) ⭐ NEW

## トラブルシューティング

### よくある問題

#### ポート競合
```bash
# 使用中のポート確認
lsof -i :80
lsof -i :3000
lsof -i :8080
lsof -i :3306
lsof -i :9099

# プロセス終了
kill -9 <PID>
```

#### データベース接続エラー
```bash
# MySQLコンテナ確認
docker-compose ps mysql

# MySQLログ確認
docker-compose logs mysql

# MySQLコンテナ再起動
docker-compose restart mysql
```

#### Firebase認証エラー
```bash
# Firebaseエミュレータ確認
docker-compose ps firebase-auth

# Firebaseログ確認
docker-compose logs firebase-auth

# Firebaseエミュレータ再起動
docker-compose restart firebase-auth
```

### デバッグ方法

#### コンテナ内でのデバッグ
```bash
# バックエンドコンテナに入る
docker-compose exec backend sh

# フロントエンドコンテナに入る
docker-compose exec frontend sh

# MySQLコンテナに入る
docker-compose exec mysql mysql -u bowlards -p bowlards_dev
```

## ライセンス

MIT License

## 貢献

プルリクエストやイシューの報告を歓迎します。

## 変更履歴

| バージョン | 日付 | 変更内容 |
|-----------|------|----------|
| 1.0.0 | 2024-01-01 | 初版作成 |
