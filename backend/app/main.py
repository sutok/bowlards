"""FastAPIメインアプリケーション"""
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from datetime import datetime
import logging
import uvicorn

from app.config import settings
from app.utils.logging import setup_logging, get_logger
from app.exceptions import (
    AuthenticationError, AuthorizationError, TokenExpiredError,
    UserNotFoundError, GameNotFoundError, InvalidRollError,
    GameCompletedError, ValidationError
)
from app.routers import users, games

# ログ設定
setup_logging()
logger = get_logger(__name__)

# FastAPIアプリケーション作成
app = FastAPI(
    title="Scoring Bowlards API",
    description="ボーリングスコア記録・管理アプリケーションのAPI",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=settings.allowed_methods,
    allow_headers=settings.allowed_headers,
)

# 信頼できるホスト設定
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"]  # 本番環境では適切に制限
)


# グローバル例外ハンドラー
@app.exception_handler(AuthenticationError)
async def authentication_exception_handler(request: Request, exc: AuthenticationError):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "code": "AUTHENTICATION_ERROR",
                "message": exc.detail
            }
        }
    )


@app.exception_handler(AuthorizationError)
async def authorization_exception_handler(request: Request, exc: AuthorizationError):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "code": "AUTHORIZATION_ERROR",
                "message": exc.detail
            }
        }
    )


@app.exception_handler(TokenExpiredError)
async def token_expired_exception_handler(request: Request, exc: TokenExpiredError):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "code": "TOKEN_EXPIRED",
                "message": exc.detail
            }
        }
    )


@app.exception_handler(UserNotFoundError)
async def user_not_found_exception_handler(request: Request, exc: UserNotFoundError):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "code": "USER_NOT_FOUND",
                "message": exc.detail
            }
        }
    )


@app.exception_handler(GameNotFoundError)
async def game_not_found_exception_handler(request: Request, exc: GameNotFoundError):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "code": "GAME_NOT_FOUND",
                "message": exc.detail
            }
        }
    )


@app.exception_handler(InvalidRollError)
async def invalid_roll_exception_handler(request: Request, exc: InvalidRollError):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "code": "INVALID_ROLL",
                "message": exc.detail
            }
        }
    )


@app.exception_handler(GameCompletedError)
async def game_completed_exception_handler(request: Request, exc: GameCompletedError):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "code": "GAME_COMPLETED",
                "message": exc.detail
            }
        }
    )


@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "code": "VALIDATION_ERROR",
                "message": exc.detail
            }
        }
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Request validation failed",
                "details": exc.errors()
            }
        }
    )


# ルートエンドポイント
@app.get("/")
async def root():
    """ルートエンドポイント"""
    return {
        "success": True,
        "data": {
            "message": "Scoring Bowlards API",
            "version": "1.0.0",
            "status": "running"
        }
    }


@app.get("/health")
async def health_check():
    """ヘルスチェック"""
    return {
        "success": True,
        "data": {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "version": "1.0.0"
        }
    }


# APIルーターを登録
app.include_router(users.router, prefix="/api/v1")
app.include_router(games.router, prefix="/api/v1")


# アプリケーション起動時のイベント
@app.on_event("startup")
async def startup_event():
    """アプリケーション起動時の処理"""
    logger.info("Scoring Bowlards API started")
    logger.info(f"Debug mode: {settings.debug}")
    logger.info(f"Log level: {settings.log_level}")


# アプリケーション終了時のイベント
@app.on_event("shutdown")
async def shutdown_event():
    """アプリケーション終了時の処理"""
    logger.info("Scoring Bowlards API shutdown")


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level=settings.log_level.lower()
    )
