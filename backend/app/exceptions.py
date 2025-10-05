"""カスタム例外クラス"""
from fastapi import HTTPException, status


class AuthenticationError(HTTPException):
    """認証エラー"""
    def __init__(self, detail: str = "Authentication failed"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail
        )


class AuthorizationError(HTTPException):
    """認可エラー"""
    def __init__(self, detail: str = "Access denied"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail
        )


class TokenExpiredError(HTTPException):
    """トークン期限切れエラー"""
    def __init__(self, detail: str = "Token expired"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail
        )


class UserNotFoundError(HTTPException):
    """ユーザーが見つからないエラー"""
    def __init__(self, detail: str = "User not found"):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail
        )


class GameNotFoundError(HTTPException):
    """ゲームが見つからないエラー"""
    def __init__(self, detail: str = "Game not found"):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail
        )


class InvalidRollError(HTTPException):
    """無効なロールエラー"""
    def __init__(self, detail: str = "Invalid roll"):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail
        )


class GameCompletedError(HTTPException):
    """ゲーム完了済みエラー"""
    def __init__(self, detail: str = "Game is already completed"):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail
        )


class ValidationError(HTTPException):
    """バリデーションエラー"""
    def __init__(self, detail: str = "Validation error"):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=detail
        )
