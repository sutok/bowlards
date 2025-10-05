.PHONY: ps psa restart up build down logs clean firestore-init test test-frontend lint-backend lint-frontend

# コンテナ一覧
ps:
	docker compose ps
psa:
	docker compose ps -a

# コンテナ再起動
restart:
	docker compose restart

# 開発環境起動
up:
	docker-compose up -d

# 開発環境再ビルド
build:
	docker compose build --no-cache

# フロントエンドのみ再ビルド（最適化版）
build-frontend:
	DOCKER_BUILDKIT=1 docker compose build --target development frontend

# フロントエンドのみ再ビルド（キャッシュクリア）
build-frontend-clean:
	DOCKER_BUILDKIT=1 docker compose build --no-cache --target development frontend

# 開発環境停止
down:
	docker-compose down

# ログ確認
logs:
	docker-compose logs -f

# 開発環境クリーンアップ
clean:
	docker-compose down -v --remove-orphans

# Firestore初期化
firestore-init:
	docker-compose exec firebase-firestore firebase emulators:exec --only firestore 'node firebase-init.js'

# バックエンドテスト
test:
	docker-compose exec backend go test ./...

# フロントエンドテスト
test-frontend:
	docker-compose exec frontend npm test

# バックエンドリント
lint-backend:
	docker-compose exec backend golangci-lint run

# フロントエンドリント
lint-frontend:
	docker-compose exec frontend npm run lint

# Firebase接続テスト
test-firebase:
	docker-compose exec backend python test_firebase_connection.py

# バックエンドシェル
shell-backend:
	docker-compose exec backend /bin/bash
