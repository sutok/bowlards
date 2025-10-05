"""ログ設定ユーティリティ"""
import logging
import structlog
from typing import Any, Dict
from app.config import settings


def setup_logging():
    """ログ設定を初期化"""
    # 基本ログ設定
    logging.basicConfig(
        level=getattr(logging, settings.log_level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # structlog設定
    if settings.log_format == "json":
        structlog.configure(
            processors=[
                structlog.stdlib.filter_by_level,
                structlog.stdlib.add_logger_name,
                structlog.stdlib.add_log_level,
                structlog.stdlib.PositionalArgumentsFormatter(),
                structlog.processors.TimeStamper(fmt="iso"),
                structlog.processors.StackInfoRenderer(),
                structlog.processors.format_exc_info,
                structlog.processors.UnicodeDecoder(),
                structlog.processors.JSONRenderer()
            ],
            context_class=dict,
            logger_factory=structlog.stdlib.LoggerFactory(),
            wrapper_class=structlog.stdlib.BoundLogger,
            cache_logger_on_first_use=True,
        )
    else:
        structlog.configure(
            processors=[
                structlog.stdlib.filter_by_level,
                structlog.stdlib.add_logger_name,
                structlog.stdlib.add_log_level,
                structlog.stdlib.PositionalArgumentsFormatter(),
                structlog.processors.TimeStamper(fmt="iso"),
                structlog.processors.StackInfoRenderer(),
                structlog.processors.format_exc_info,
                structlog.processors.UnicodeDecoder(),
                structlog.dev.ConsoleRenderer()
            ],
            context_class=dict,
            logger_factory=structlog.stdlib.LoggerFactory(),
            wrapper_class=structlog.stdlib.BoundLogger,
            cache_logger_on_first_use=True,
        )


def get_logger(name: str) -> structlog.BoundLogger:
    """ロガーを取得"""
    return structlog.get_logger(name)


class AuthLogger:
    """認証ログヘルパー"""
    
    @staticmethod
    def log_authentication_success(user_id: str, email: str):
        """認証成功ログ"""
        logger = get_logger("auth")
        logger.info(
            event="auth_success",
            user_id=user_id,
            email=email
        )
    
    @staticmethod
    def log_authentication_failure(error: str, user_id: str = None):
        """認証失敗ログ"""
        logger = get_logger("auth")
        logger.warning(
            event="auth_failure",
            error=error,
            user_id=user_id
        )
    
    @staticmethod
    def log_token_verification(token: str, success: bool):
        """トークン検証ログ"""
        logger = get_logger("auth")
        logger.info(
            event="token_verification",
            success=success
        )


class GameLogger:
    """ゲームログヘルパー"""
    
    @staticmethod
    def log_game_created(game_id: str, user_id: str):
        """ゲーム作成ログ"""
        logger = get_logger("game")
        logger.info(
            event="game_created",
            game_id=game_id,
            user_id=user_id
        )
    
    @staticmethod
    def log_roll_added(game_id: str, user_id: str, frame_number: int, pin_count: int):
        """ロール追加ログ"""
        logger = get_logger("game")
        logger.info(
            event="roll_added",
            game_id=game_id,
            user_id=user_id,
            frame_number=frame_number,
            pin_count=pin_count
        )
    
    @staticmethod
    def log_game_completed(game_id: str, user_id: str, total_score: int):
        """ゲーム完了ログ"""
        logger = get_logger("game")
        logger.info(
            event="game_completed",
            game_id=game_id,
            user_id=user_id,
            total_score=total_score
        )
