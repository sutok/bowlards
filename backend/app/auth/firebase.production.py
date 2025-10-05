"""本番環境用Firebase認証クライアント"""
import firebase_admin
from firebase_admin import credentials, auth
from typing import Dict, Any
import logging
from app.config import settings

logger = logging.getLogger(__name__)


class FirebaseAuthProduction:
    """本番環境用Firebase認証クライアント"""
    
    def __init__(self):
        self._initialize_firebase()
    
    def _initialize_firebase(self):
        """Firebase Admin SDKを初期化（本番環境用）"""
        if not firebase_admin._apps:
            try:
                if settings.firebase_credentials_path:
                    # サービスアカウントキーファイルから認証情報を読み込み
                    cred = credentials.Certificate(settings.firebase_credentials_path)
                    firebase_admin.initialize_app(cred)
                    logger.info(f"Firebase initialized with credentials file: {settings.firebase_credentials_path}")
                elif settings.firebase_private_key and settings.firebase_client_email:
                    # 環境変数から認証情報を読み込み
                    cred_dict = {
                        "type": "service_account",
                        "project_id": settings.firebase_project_id,
                        "private_key": settings.firebase_private_key.replace('\\n', '\n'),
                        "client_email": settings.firebase_client_email,
                        "token_uri": "https://oauth2.googleapis.com/token"
                    }
                    cred = credentials.Certificate(cred_dict)
                    firebase_admin.initialize_app(cred)
                    logger.info("Firebase initialized with environment variables")
                else:
                    # 本番環境では認証情報が必須
                    logger.error("No Firebase credentials provided for production environment")
                    raise ValueError("Firebase credentials are required for production environment")
            except Exception as e:
                logger.error(f"Failed to initialize Firebase: {e}")
                raise
    
    async def verify_token(self, token: str) -> Dict[str, Any]:
        """Firebase IDトークンを検証"""
        try:
            decoded_token = auth.verify_id_token(token)
            logger.debug(f"Token verified for user: {decoded_token.get('uid')}")
            return decoded_token
        except auth.InvalidIdTokenError:
            logger.warning("Invalid ID token provided")
            raise ValueError("Invalid ID token")
        except auth.ExpiredIdTokenError:
            logger.warning("Expired ID token provided")
            raise ValueError("Expired ID token")
        except Exception as e:
            logger.error(f"Token verification failed: {e}")
            raise ValueError(f"Token verification failed: {str(e)}")
    
    async def get_user(self, uid: str) -> Dict[str, Any]:
        """ユーザー情報を取得"""
        try:
            user_record = auth.get_user(uid)
            return {
                "uid": user_record.uid,
                "email": user_record.email,
                "display_name": user_record.display_name,
                "photo_url": user_record.photo_url,
                "email_verified": user_record.email_verified,
                "disabled": user_record.disabled
            }
        except auth.UserNotFoundError:
            logger.warning(f"User not found: {uid}")
            raise ValueError("User not found")
        except Exception as e:
            logger.error(f"Failed to get user {uid}: {e}")
            raise ValueError(f"Failed to get user: {str(e)}")


# 本番環境用シングルトンインスタンス
firebase_auth_production = FirebaseAuthProduction()
