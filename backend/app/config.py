"""設定管理モジュール"""
from pydantic_settings import BaseSettings
from typing import List, Optional
import os


class Settings(BaseSettings):
    """アプリケーション設定"""
    
    # サーバー設定
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = False
    
    # Firebase設定
    firebase_project_id: str
    firebase_credentials_path: Optional[str] = None
    firebase_private_key: Optional[str] = None
    firebase_client_email: Optional[str] = None
    
    # ログ設定
    log_level: str = "INFO"
    log_format: str = "json"
    
    # セキュリティ設定
    secret_key: str = "your-secret-key-here"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # CORS設定
    allowed_origins: List[str] = [
        "http://localhost:3000",      # 直接アクセス（開発用）
        "http://localhost:13000",     # Dockerフロントエンド
        "http://localhost:11080"      # Nginx経由
    ]
    allowed_methods: List[str] = ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    allowed_headers: List[str] = ["*"]
    
    # レート制限設定
    rate_limit_calls: int = 1000
    rate_limit_period: int = 3600
    
    # Firestoreエミュレータ設定
    firestore_emulator_host: Optional[str] = None
    firestore_emulator_port: Optional[int] = None
    
    # Firebase認証エミュレータ設定
    firebase_auth_emulator_host: Optional[str] = None
    firebase_auth_emulator_port: Optional[int] = None
    
    class Config:
        env_file = ".env"
        env_prefix = "APP_"
        case_sensitive = False


# グローバル設定インスタンス
settings = Settings()


def get_settings() -> Settings:
    """設定インスタンスを取得"""
    return settings
