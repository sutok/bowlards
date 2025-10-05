"""ユーザーサービス"""
from typing import Optional
import logging
from app.repositories.user_repository import UserRepository
from app.models.user import UserCreate, UserUpdate, UserResponse, UserSchema
from app.exceptions import UserNotFoundError
from app.utils.logging import get_logger

logger = get_logger(__name__)


class UserService:
    """ユーザーサービス"""
    
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo
    
    async def create_user(self, user_data: UserCreate) -> UserResponse:
        """ユーザーを作成"""
        try:
            # 既存ユーザーチェック
            existing_user = await self.user_repo.get_by_uid(user_data.uid)
            if existing_user:
                raise ValueError("User already exists")
            
            # ユーザー作成
            user_schema = await self.user_repo.create(user_data)
            
            logger.info(f"User created successfully: {user_schema.uid}")
            return UserResponse(
                id=user_schema.id,
                uid=user_schema.uid,
                email=user_schema.email,
                display_name=user_schema.display_name,
                photo_url=user_schema.photo_url,
                created_at=user_schema.created_at,
                updated_at=user_schema.updated_at
            )
            
        except ValueError as e:
            logger.warning(f"User creation failed: {e}")
            raise
        except Exception as e:
            logger.error(f"Failed to create user: {e}")
            raise
    
    async def get_user_profile(self, user_id: str) -> UserResponse:
        """ユーザープロフィールを取得"""
        try:
            user_schema = await self.user_repo.get_by_id(user_id)
            if not user_schema:
                raise UserNotFoundError()
            
            return UserResponse(
                id=user_schema.id,
                uid=user_schema.uid,
                email=user_schema.email,
                display_name=user_schema.display_name,
                photo_url=user_schema.photo_url,
                created_at=user_schema.created_at,
                updated_at=user_schema.updated_at
            )
            
        except UserNotFoundError:
            raise
        except Exception as e:
            logger.error(f"Failed to get user profile {user_id}: {e}")
            raise
    
    async def update_user_profile(self, user_id: str, user_data: UserUpdate) -> UserResponse:
        """ユーザープロフィールを更新"""
        try:
            # 既存ユーザーチェック
            existing_user = await self.user_repo.get_by_id(user_id)
            if not existing_user:
                raise UserNotFoundError()
            
            # ユーザー更新
            updated_user = await self.user_repo.update(user_id, user_data)
            
            logger.info(f"User profile updated successfully: {user_id}")
            return UserResponse(
                id=updated_user.id,
                uid=updated_user.uid,
                email=updated_user.email,
                display_name=updated_user.display_name,
                photo_url=updated_user.photo_url,
                created_at=updated_user.created_at,
                updated_at=updated_user.updated_at
            )
            
        except UserNotFoundError:
            raise
        except Exception as e:
            logger.error(f"Failed to update user profile {user_id}: {e}")
            raise
    
    async def delete_user(self, user_id: str) -> bool:
        """ユーザーを削除"""
        try:
            # 既存ユーザーチェック
            existing_user = await self.user_repo.get_by_id(user_id)
            if not existing_user:
                raise UserNotFoundError()
            
            # ユーザー削除
            await self.user_repo.delete(user_id)
            
            logger.info(f"User deleted successfully: {user_id}")
            return True
            
        except UserNotFoundError:
            raise
        except Exception as e:
            logger.error(f"Failed to delete user {user_id}: {e}")
            raise
    
    async def get_or_create_user(self, uid: str, email: str, display_name: str, photo_url: Optional[str] = None) -> UserResponse:
        """ユーザーを取得または作成"""
        try:
            # 既存ユーザーを取得
            existing_user = await self.user_repo.get_by_uid(uid)
            if existing_user:
                return UserResponse(
                    id=existing_user.id,
                    uid=existing_user.uid,
                    email=existing_user.email,
                    display_name=existing_user.display_name,
                    photo_url=existing_user.photo_url,
                    created_at=existing_user.created_at,
                    updated_at=existing_user.updated_at
                )
            
            # 新規ユーザー作成
            user_data = UserCreate(
                uid=uid,
                email=email,
                display_name=display_name,
                photo_url=photo_url
            )
            
            return await self.create_user(user_data)
            
        except Exception as e:
            logger.error(f"Failed to get or create user {uid}: {e}")
            raise
