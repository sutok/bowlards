# FastAPI用Dockerfile (uv使用)
FROM python:3.13-slim AS builder

# 作業ディレクトリを設定
WORKDIR /app

# システムパッケージを更新し、必要なパッケージをインストール
RUN apt-get update && apt-get install -y \
    curl \
    gcc \
    g++ \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# uvのインストール
RUN pip install uv

# pyproject.tomlをコピー
COPY backend/pyproject.toml ./

# uv.lockファイルが存在する場合はコピー（オプション）
COPY backend/uv.lock* ./

# 依存関係のインストール
# uv.lockが存在する場合はfrozen、存在しない場合は通常インストール
RUN if [ -f uv.lock ]; then \
        echo "Using frozen lockfile"; \
        uv sync --frozen; \
    else \
        echo "No lockfile found, installing dependencies"; \
        uv sync; \
    fi

# 本番用の軽量なイメージ
FROM python:3.13-slim

# 作業ディレクトリを設定
WORKDIR /app

# システムパッケージを更新し、必要なパッケージをインストール
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# uvをインストール
RUN pip install uv

# ビルドステージから仮想環境をコピー
COPY --from=builder /app/.venv /app/.venv

# アプリケーションコードをコピー
COPY backend/ .

# 仮想環境のPythonシンボリックリンクを修正
RUN rm -f /app/.venv/bin/python /app/.venv/bin/python3 /app/.venv/bin/python3.11 /app/.venv/bin/python3.13 && \
    ln -s /usr/local/bin/python3 /app/.venv/bin/python && \
    ln -s /usr/local/bin/python3 /app/.venv/bin/python3 && \
    ln -s /usr/local/bin/python3 /app/.venv/bin/python3.13

# 非rootユーザーを作成
RUN useradd --create-home --shell /bin/bash app \
    && chown -R app:app /app
USER app

# 仮想環境をアクティベート
ENV PATH="/app/.venv/bin:$PATH"

# ポートを公開
EXPOSE 8000

# ヘルスチェック
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# アプリケーションを実行
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]