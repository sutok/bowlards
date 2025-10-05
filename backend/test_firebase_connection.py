#!/usr/bin/env python3
"""Firebase接続テストスクリプト"""
import os
import sys
import logging
from pathlib import Path

# プロジェクトルートをパスに追加
sys.path.append(str(Path(__file__).parent))

from app.auth.firebase import firebase_auth
from app.config import settings

# ログ設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def test_firebase_connection():
    """Firebase接続をテスト"""
    try:
        logger.info("=== Firebase接続テスト開始 ===")
        
        # 設定情報を表示
        logger.info(f"Firebase Project ID: {settings.firebase_project_id}")
        logger.info(f"Firebase Credentials Path: {settings.firebase_credentials_path}")
        
        # 認証情報ファイルの存在確認
        if settings.firebase_credentials_path:
            if os.path.exists(settings.firebase_credentials_path):
                logger.info("✅ 認証情報ファイルが存在します")
            else:
                logger.error("❌ 認証情報ファイルが見つかりません")
                return False
        
        # Firebase認証クライアントの初期化テスト
        logger.info("Firebase認証クライアントの初期化をテスト中...")
        
        # 認証クライアントが正常に初期化されているか確認
        if firebase_auth:
            logger.info("✅ Firebase認証クライアントが正常に初期化されました")
        else:
            logger.error("❌ Firebase認証クライアントの初期化に失敗しました")
            return False
        
        logger.info("=== Firebase接続テスト完了 ===")
        return True
        
    except Exception as e:
        logger.error(f"❌ Firebase接続テストでエラーが発生しました: {e}")
        return False


if __name__ == "__main__":
    success = test_firebase_connection()
    if success:
        print("✅ Firebase接続テストが成功しました")
        sys.exit(0)
    else:
        print("❌ Firebase接続テストが失敗しました")
        sys.exit(1)
