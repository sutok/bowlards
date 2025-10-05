#!/bin/bash
set -e

# credentialsディレクトリが存在する場合、読み取り権限を設定
if [ -d "/app/credentials" ]; then
    echo "Setting permissions for credentials directory..."
    chmod -R 755 /app/credentials
    find /app/credentials -type f -exec chmod 644 {} \;
fi

# 環境変数のPATHを設定
export PATH="/app/.venv/bin:$PATH"

# appユーザーとしてアプリケーションを実行
exec gosu app:app "$@"

