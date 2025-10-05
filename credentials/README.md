# 認証情報ディレクトリ

このディレクトリには、Firebaseサービスアカウントキーファイルなどの機密情報を配置します。

## ファイル配置

```
credentials/
├── firebase-service-account.json  # Firebaseサービスアカウントキー
└── .gitignore                     # 機密ファイルを除外
```

## セキュリティ注意事項

- **絶対にGitにコミットしないでください**
- ファイルの権限を適切に設定してください（600推奨）
- 本番環境では環境変数での認証情報設定を推奨します

## ファイル権限の設定

```bash
chmod 600 credentials/firebase-service-account.json
```

## 環境変数での認証（推奨）

本番環境では、ファイルではなく環境変数での認証情報設定を推奨します：
