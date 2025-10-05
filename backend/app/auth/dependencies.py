"""認証依存関係"""
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Dict, Any
import logging
from app.auth.firebase import firebase_auth
from app.exceptions import AuthenticationError, TokenExpiredError

logger = logging.getLogger(__name__)

# HTTP Bearer認証スキーム
security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> Dict[str, Any]:
    """現在のユーザーを取得"""
    try:
        token = credentials.credentials
        decoded_token = await firebase_auth.verify_token(token)
        return decoded_token
    except ValueError as e:
        error_msg = str(e)
        if "expired" in error_msg.lower():
            raise TokenExpiredError(error_msg)
        else:
            raise AuthenticationError(error_msg)


async def get_current_user_id(
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> str:
    """現在のユーザーIDを取得"""
    uid = current_user.get("uid")
    if not uid:
        raise AuthenticationError("User ID not found in token")
    return uid


async def get_current_user_email(
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> str:
    """現在のユーザーメールアドレスを取得"""
    email = current_user.get("email")
    if not email:
        raise AuthenticationError("Email not found in token")
    return email


async def get_optional_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> Dict[str, Any]:
    """オプショナルな現在のユーザーを取得（認証なしでもアクセス可能）"""
    try:
        token = credentials.credentials
        decoded_token = await firebase_auth.verify_token(token)
        return decoded_token
    except Exception as e:
        logger.debug(f"Optional auth failed: {e}")
        return None
