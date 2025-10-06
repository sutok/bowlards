"""ユーザーリポジトリ"""
from google.cloud import firestore
from typing import List, Optional
from datetime import datetime
import logging
from app.models.user import UserSchema, UserCreate, UserUpdate
from app.exceptions import UserNotFoundError

logger = logging.getLogger(__name__)


class UserRepository:
    """ユーザーリポジトリ"""
    
    def __init__(self, db: firestore.Client):
        self.db = db
        self.collection = "users"
    
    async def create(self, user_data: UserCreate) -> UserSchema:
        """ユーザーを作成"""
        try:
            doc_ref = self.db.collection(self.collection).document(user_data.uid)
            
            # 既存チェック
            if doc_ref.get().exists:
                raise ValueError("User already exists")
            
            user_dict = user_data.dict()
            user_dict['id'] = user_data.uid
            user_dict['created_at'] = firestore.SERVER_TIMESTAMP
            user_dict['updated_at'] = firestore.SERVER_TIMESTAMP
            
            doc_ref.set(user_dict)
            
            # 作成されたユーザーを取得
            doc = doc_ref.get()
            user_data_dict = doc.to_dict()
            user_data_dict['id'] = doc.id
            
            logger.info(f"User created: {user_data.uid}")
            return UserSchema(**user_data_dict)
            
        except Exception as e:
            logger.error(f"Failed to create user {user_data.uid}: {e}")
            raise
    
    async def get_by_id(self, user_id: str) -> Optional[UserSchema]:
        """ユーザーIDでユーザーを取得"""
        try:
            doc = self.db.collection(self.collection).document(user_id).get()
            
            if not doc.exists:
                return None
            
            user_data = doc.to_dict()
            user_data['id'] = doc.id
            
            return UserSchema(**user_data)
            
        except Exception as e:
            logger.error(f"Failed to get user {user_id}: {e}")
            raise
    
    async def get_by_uid(self, uid: str) -> Optional[UserSchema]:
        """Firebase UIDでユーザーを取得"""
        try:
            logger.info(f"🔍 [REPO] Searching for user with uid: {uid}")
            query = self.db.collection(self.collection).where("uid", "==", uid).limit(1)
            docs = query.stream()

            for doc in docs:
                logger.info(f"✅ [REPO] User found: {doc.id}")
                user_data = doc.to_dict()
                user_data['id'] = doc.id
                return UserSchema(**user_data)

            logger.info(f"ℹ️ [REPO] User not found with uid: {uid}")
            return None

        except Exception as e:
            logger.error(f"❌ [REPO] Failed to get user by UID {uid}: {e}", exc_info=True)
            raise
    
    async def update(self, user_id: str, user_data: UserUpdate) -> UserSchema:
        """ユーザーを更新"""
        try:
            doc_ref = self.db.collection(self.collection).document(user_id)
            
            # 既存チェック
            if not doc_ref.get().exists:
                raise UserNotFoundError()
            
            update_data = user_data.dict(exclude_unset=True)
            update_data['updated_at'] = firestore.SERVER_TIMESTAMP
            
            doc_ref.update(update_data)
            
            # 更新されたユーザーを取得
            doc = doc_ref.get()
            user_data_dict = doc.to_dict()
            user_data_dict['id'] = doc.id
            
            logger.info(f"User updated: {user_id}")
            return UserSchema(**user_data_dict)
            
        except UserNotFoundError:
            raise
        except Exception as e:
            logger.error(f"Failed to update user {user_id}: {e}")
            raise
    
    async def delete(self, user_id: str) -> bool:
        """ユーザーを削除"""
        try:
            doc_ref = self.db.collection(self.collection).document(user_id)
            
            # 既存チェック
            if not doc_ref.get().exists:
                raise UserNotFoundError()
            
            doc_ref.delete()
            
            logger.info(f"User deleted: {user_id}")
            return True
            
        except UserNotFoundError:
            raise
        except Exception as e:
            logger.error(f"Failed to delete user {user_id}: {e}")
            raise
    
    async def exists(self, user_id: str) -> bool:
        """ユーザーの存在チェック（ドキュメントIDで検索）"""
        try:
            doc = self.db.collection(self.collection).document(user_id).get()
            return doc.exists
        except Exception as e:
            logger.error(f"Failed to check user existence {user_id}: {e}")
            raise
    
    async def exists_by_uid(self, uid: str) -> bool:
        """ユーザーの存在チェック（UIDで検索）"""
        try:
            user = await self.get_by_uid(uid)
            return user is not None
        except Exception as e:
            logger.error(f"Failed to check user existence by UID {uid}: {e}")
            raise
