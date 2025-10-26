"""Firebase認証クライアント（本番環境用）"""
import firebase_admin
from firebase_admin import credentials, auth
from typing import Dict, Any
import logging
import os
from app.config import settings

logger = logging.getLogger(__name__)


class FirebaseAuth:
    """Firebase認証クライアント（本番環境用）"""

    def __init__(self):
        self._initialize_firebase()

    def _initialize_firebase(self):
        """Firebase Admin SDKを初期化（エミュレータ対応）"""
        if not firebase_admin._apps:
            try:
                # エミュレータ変数の初期化（未定義または空文字の場合はNone）
                firestore_emulator = os.environ.get('FIRESTORE_EMULATOR_HOST') or None
                auth_emulator = os.environ.get('FIREBASE_AUTH_EMULATOR_HOST') or None

                # エミュレータホストとポートを設定から環境変数に設定
                if settings.firestore_emulator_host and settings.firestore_emulator_port:
                    emulator_host = f"{settings.firestore_emulator_host}:{settings.firestore_emulator_port}"
                    os.environ['FIRESTORE_EMULATOR_HOST'] = emulator_host
                    firestore_emulator = emulator_host
                    logger.info(f"Using Firestore emulator at {emulator_host}")

                if settings.firebase_auth_emulator_host and settings.firebase_auth_emulator_port:
                    auth_emulator_host = f"{settings.firebase_auth_emulator_host}:{settings.firebase_auth_emulator_port}"
                    os.environ['FIREBASE_AUTH_EMULATOR_HOST'] = auth_emulator_host
                    auth_emulator = auth_emulator_host
                    logger.info(f"Using Firebase Auth emulator at {auth_emulator_host}")

                # エミュレータモードの場合、環境変数のダミー認証情報を使用
                if firestore_emulator or auth_emulator:
                    # GOOGLE_APPLICATION_CREDENTIALSから認証情報を読み込む
                    # (Dockerfileで/tmp/dummy-credentials.jsonを作成済み)
                    firebase_admin.initialize_app(options={'projectId': settings.firebase_project_id})
                    logger.info(f"🔧 Firebase initialized in emulator mode for project: {settings.firebase_project_id}")
                # 本番モード: 認証情報が必要
                elif settings.firebase_credentials_path and os.path.exists(settings.firebase_credentials_path):
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
                    logger.error("No Firebase credentials or emulator configuration provided")
                    logger.error(f"Credentials path: {settings.firebase_credentials_path}")
                    logger.error(f"Firestore emulator host: {settings.firestore_emulator_host}:{settings.firestore_emulator_port}")
                    logger.error(f"Auth emulator host: {settings.firebase_auth_emulator_host}:{settings.firebase_auth_emulator_port}")
                    raise ValueError("Firebase credentials or emulator configuration required")
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


# シングルトンインスタンス
firebase_auth = FirebaseAuth()
