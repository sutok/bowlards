"""ユーザーAPIルーター"""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict, Any
from app.auth.dependencies import get_current_user, get_current_user_id
from app.services.user_service import UserService
from app.models.user import UserResponse, UserUpdate
from app.models.common import success_response, error_response
from app.exceptions import UserNotFoundError
from app.utils.logging import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/users", tags=["users"])


def get_user_service() -> UserService:
    """ユーザーサービスの依存関係注入"""
    from app.dependencies import get_firestore_client
    from app.repositories.user_repository import UserRepository
    
    db = get_firestore_client()
    user_repo = UserRepository(db)
    return UserService(user_repo)


@router.get("/profile", response_model=Dict[str, Any])
async def get_user_profile(
    current_user: Dict[str, Any] = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service)
):
    """
    ユーザープロフィールを取得（存在しない場合は自動作成）

    Firebase認証トークンからユーザー情報を取得し、
    Firestoreに存在しない場合は自動的に作成します。
    """
    try:
        logger.info(f"👤 [ROUTER] get_user_profile called")
        uid = current_user.get("uid")
        email = current_user.get("email", "")
        display_name = current_user.get("name") or current_user.get("display_name") or email.split("@")[0]
        photo_url = current_user.get("picture") or current_user.get("photo_url")

        logger.info(f"👤 [ROUTER] User info - uid: {uid}, email: {email}, display_name: {display_name}")

        # ユーザーを取得または作成
        user = await user_service.get_or_create_user(
            uid=uid,
            email=email,
            display_name=display_name,
            photo_url=photo_url
        )

        logger.info(f"✅ [ROUTER] User profile retrieved successfully: {user.id}")
        return success_response(data=user.dict())

    except Exception as e:
        logger.error(f"❌ [ROUTER] Failed to get or create user profile: {e}", exc_info=True)
        return error_response("GET_FAILED", f"Failed to get user profile: {str(e)}")


@router.put("/profile", response_model=Dict[str, Any])
async def update_user_profile(
    user_data: UserUpdate,
    current_user: Dict[str, Any] = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service)
):
    """ユーザープロフィールを更新"""
    try:
        uid = current_user.get("uid")
        
        # まずユーザーを取得（UIDで検索）
        from app.repositories.user_repository import UserRepository
        from app.dependencies import get_firestore_client
        
        db = get_firestore_client()
        user_repo = UserRepository(db)
        existing_user = await user_repo.get_by_uid(uid)
        
        if not existing_user:
            return error_response("USER_NOT_FOUND", "User not found")
        
        # ユーザーを更新（ドキュメントIDで更新）
        user = await user_service.update_user_profile(existing_user.id, user_data)
        return success_response(data=user.dict())
        
    except UserNotFoundError:
        return error_response("USER_NOT_FOUND", "User not found")
    except Exception as e:
        logger.error(f"Failed to update user profile: {e}")
        return error_response("UPDATE_FAILED", "Failed to update user profile")


@router.delete("/profile", response_model=Dict[str, Any])
async def delete_user(
    current_user: Dict[str, Any] = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service)
):
    """ユーザーを削除"""
    try:
        uid = current_user.get("uid")
        
        # まずユーザーを取得（UIDで検索）
        from app.repositories.user_repository import UserRepository
        from app.dependencies import get_firestore_client
        
        db = get_firestore_client()
        user_repo = UserRepository(db)
        existing_user = await user_repo.get_by_uid(uid)
        
        if not existing_user:
            return error_response("USER_NOT_FOUND", "User not found")
        
        # ユーザーを削除（ドキュメントIDで削除）
        await user_service.delete_user(existing_user.id)
        return success_response(data={"message": "User deleted successfully"})
        
    except UserNotFoundError:
        return error_response("USER_NOT_FOUND", "User not found")
    except Exception as e:
        logger.error(f"Failed to delete user: {e}")
        return error_response("DELETE_FAILED", "Failed to delete user")
