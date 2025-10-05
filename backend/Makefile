# Makefile for Scoring Bowlards Backend

.PHONY: help install install-dev run test lint format clean docker-build docker-run

# デフォルトターゲット
help:
	@echo "Available targets:"
	@echo "  install      - Install production dependencies"
	@echo "  install-dev  - Install development dependencies"
	@echo "  run          - Run the application"
	@echo "  test         - Run tests"
	@echo "  lint         - Run linting"
	@echo "  format       - Format code"
	@echo "  clean        - Clean cache files"
	@echo "  docker-build - Build Docker image"
	@echo "  docker-run   - Run Docker container"

# 依存関係のインストール
install:
	uv pip install -e .

# 開発用依存関係のインストール
install-dev:
	uv pip install -e ".[dev]"

# アプリケーション実行
run:
	uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# テスト実行
test:
	uv run pytest

# カバレッジ付きテスト実行
test-cov:
	uv run pytest --cov=app --cov-report=html --cov-report=term-missing

# リント実行
lint:
	uv run flake8 app/
	uv run mypy app/

# コードフォーマット
format:
	uv run black app/
	uv run isort app/

# キャッシュファイルのクリーンアップ
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf htmlcov
	rm -rf dist
	rm -rf build

# Dockerイメージビルド
docker-build:
	docker build -f docker/backend/Dockerfile -t bowlards-backend .

# Dockerコンテナ実行
docker-run:
	docker run -p 8000:8000 --env-file .env bowlards-backend

# 開発環境セットアップ
setup-dev: install-dev
	@echo "Development environment setup complete!"
	@echo "Run 'make run' to start the development server"

# 本番環境セットアップ
setup-prod: install
	@echo "Production environment setup complete!"
	@echo "Run 'make run' to start the production server"
