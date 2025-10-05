# ベースイメージ（最新のLTS版を使用）
FROM node:24-slim AS base

# 作業ディレクトリを設定
WORKDIR /app

# パッケージマネージャーのキャッシュを有効化
RUN npm config set cache /tmp/.npm

# 依存関係インストール用のステージ
FROM base AS deps

# package.jsonとpackage-lock.jsonをコピー
COPY package*.json ./

# 本番用依存関係をインストール（npm ciを使用）
RUN npm ci --only=production --no-audit --no-fund

# 開発用依存関係も含めてインストール
FROM base AS dev-deps
COPY package*.json ./
RUN npm ci --no-audit --no-fund

# 開発環境用のステージ
FROM base AS development

# 開発用依存関係をコピー
COPY --from=dev-deps /app/node_modules ./node_modules

# アプリケーションコードをコピー
COPY . .

# ポートを公開
EXPOSE 3000

# 開発サーバーを起動（ホットリロード有効）
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]