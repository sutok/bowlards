"""ゲームサービス"""
from typing import List
import logging
from datetime import datetime
from app.repositories.game_repository import GameRepository
from app.repositories.user_repository import UserRepository
from app.models.game import (
    GameCreate, GameResponse, RollRequest, GameHistoryRequest, 
    GameHistoryResponse, GameStatistics, CompletedGameRequest, Frame
)
from app.exceptions import GameNotFoundError, InvalidRollError, GameCompletedError
from app.utils.scoring import calculate_score, create_initial_frames
from app.utils.logging import get_logger, GameLogger

logger = get_logger(__name__)


class GameService:
    """ゲームサービス"""
    
    def __init__(self, game_repo: GameRepository, user_repo: UserRepository):
        self.game_repo = game_repo
        self.user_repo = user_repo
    
    async def create_game(self, user_id: str) -> GameResponse:
        """新しいゲームを作成"""
        try:
            # ユーザー存在チェック（UIDで検索）
            user_exists = await self.user_repo.exists_by_uid(user_id)
            if not user_exists:
                raise ValueError("User not found")
            
            # 初期フレームを作成
            frames = create_initial_frames()
            
            # ゲームデータを作成
            game_data = GameCreate(
                user_id=user_id,
                total_score=0,
                frames=frames,
                status="playing"
            )
            
            # ゲーム作成
            game_schema = await self.game_repo.create(game_data)
            
            GameLogger.log_game_created(game_schema.id, user_id)
            
            return GameResponse(
                id=game_schema.id,
                user_id=game_schema.user_id,
                total_score=game_schema.total_score,
                frames=game_schema.frames,
                status=game_schema.status,
                played_at=game_schema.played_at,
                created_at=game_schema.created_at,
                updated_at=game_schema.updated_at
            )
            
        except ValueError as e:
            logger.warning(f"Game creation failed: {e}")
            raise
        except Exception as e:
            logger.error(f"Failed to create game: {e}")
            raise
    
    async def get_game(self, game_id: str, user_id: str) -> GameResponse:
        """ゲームを取得"""
        try:
            game_schema = await self.game_repo.get_by_id(game_id, user_id)
            if not game_schema:
                raise GameNotFoundError()
            
            return GameResponse(
                id=game_schema.id,
                user_id=game_schema.user_id,
                total_score=game_schema.total_score,
                frames=game_schema.frames,
                status=game_schema.status,
                played_at=game_schema.played_at,
                created_at=game_schema.created_at,
                updated_at=game_schema.updated_at
            )
            
        except GameNotFoundError:
            raise
        except Exception as e:
            logger.error(f"Failed to get game {game_id}: {e}")
            raise
    
    async def add_roll(self, game_id: str, user_id: str, roll: RollRequest) -> GameResponse:
        """ロールを追加"""
        try:
            # ゲームを取得
            game_schema = await self.game_repo.get_by_id(game_id, user_id)
            if not game_schema:
                raise GameNotFoundError()
            
            # ゲーム完了チェック
            if game_schema.status == "completed":
                raise GameCompletedError()
            
            # ロールバリデーション
            frame_index = roll.frame_number - 1
            frame = game_schema.frames[frame_index]
            
            # フレーム完了チェック
            if frame.is_completed:
                raise InvalidRollError("Frame is already completed")
            
            # ピン数バリデーション
            if roll.frame_number < 10:
                # 1-9フレーム
                if len(frame.rolls) == 0 and roll.pin_count == 10:
                    # ストライク
                    pass
                elif len(frame.rolls) == 1:
                    # 2投目
                    if frame.rolls[0] + roll.pin_count > 10:
                        raise InvalidRollError("Total pins cannot exceed 10")
                else:
                    raise InvalidRollError("Invalid roll for this frame")
            else:
                # 10フレーム目
                if len(frame.rolls) == 0 and roll.pin_count == 10:
                    # ストライク
                    pass
                elif len(frame.rolls) == 1:
                    # 2投目
                    if not frame.is_strike and frame.rolls[0] + roll.pin_count > 10:
                        raise InvalidRollError("Total pins cannot exceed 10")
                elif len(frame.rolls) == 2:
                    # 3投目
                    if frame.is_strike or frame.is_spare:
                        pass
                    else:
                        raise InvalidRollError("No third roll allowed for this frame")
                else:
                    raise InvalidRollError("Invalid roll for this frame")
            
            # スコア計算
            updated_game = calculate_score(game_schema, roll)
            
            # ゲーム更新
            updated_game_schema = await self.game_repo.update(game_id, updated_game)
            
            GameLogger.log_roll_added(game_id, user_id, roll.frame_number, roll.pin_count)
            
            # ゲーム完了チェック
            if updated_game_schema.status == "completed":
                GameLogger.log_game_completed(game_id, user_id, updated_game_schema.total_score)
            
            return GameResponse(
                id=updated_game_schema.id,
                user_id=updated_game_schema.user_id,
                total_score=updated_game_schema.total_score,
                frames=updated_game_schema.frames,
                status=updated_game_schema.status,
                played_at=updated_game_schema.played_at,
                created_at=updated_game_schema.created_at,
                updated_at=updated_game_schema.updated_at
            )
            
        except (GameNotFoundError, InvalidRollError, GameCompletedError):
            raise
        except Exception as e:
            logger.error(f"Failed to add roll to game {game_id}: {e}")
            raise
    
    async def delete_game(self, game_id: str, user_id: str) -> bool:
        """ゲームを削除"""
        try:
            await self.game_repo.delete(game_id, user_id)
            logger.info(f"Game deleted successfully: {game_id}")
            return True
            
        except GameNotFoundError:
            raise
        except Exception as e:
            logger.error(f"Failed to delete game {game_id}: {e}")
            raise
    
    async def get_game_history(self, user_id: str, history_request: GameHistoryRequest) -> GameHistoryResponse:
        """ゲーム履歴を取得"""
        try:
            history_response = await self.game_repo.get_user_games(user_id, history_request)
            
            # GameSchemaをGameResponseに変換
            games = []
            for game_schema in history_response.games:
                games.append(GameResponse(
                    id=game_schema.id,
                    user_id=game_schema.user_id,
                    total_score=game_schema.total_score,
                    frames=game_schema.frames,
                    status=game_schema.status,
                    played_at=game_schema.played_at,
                    created_at=game_schema.created_at,
                    updated_at=game_schema.updated_at
                ))
            
            return GameHistoryResponse(
                games=games,
                total=history_response.total,
                limit=history_response.limit,
                offset=history_response.offset
            )
            
        except Exception as e:
            logger.error(f"Failed to get game history for user {user_id}: {e}")
            raise
    
    async def get_game_statistics(self, user_id: str) -> GameStatistics:
        """ゲーム統計を取得"""
        try:
            stats_dict = await self.game_repo.get_user_statistics(user_id)
            
            return GameStatistics(
                total_games=stats_dict["total_games"],
                completed_games=stats_dict["completed_games"],
                average_score=stats_dict["average_score"],
                highest_score=stats_dict["highest_score"],
                lowest_score=stats_dict["lowest_score"],
                strike_count=stats_dict["strike_count"],
                spare_count=stats_dict["spare_count"],
                perfect_games=stats_dict["perfect_games"],
                turkey_count=stats_dict["turkey_count"]
            )
            
        except Exception as e:
            logger.error(f"Failed to get game statistics for user {user_id}: {e}")
            raise
    
    async def save_completed_game_with_uid(self, user_id: str, game_data: CompletedGameRequest) -> GameResponse:
        """完了したゲームを保存（認証済みユーザーIDを使用）"""
        try:
            # ユーザー存在チェック（UIDで検索）
            user_exists = await self.user_repo.exists_by_uid(user_id)
            if not user_exists:
                raise ValueError("User not found")
            
            # フロントエンドのフレームをバックエンド形式に変換
            backend_frames = []
            for frontend_frame in game_data.frames:
                rolls = []
                if frontend_frame.firstRoll is not None:
                    rolls.append(frontend_frame.firstRoll)
                if frontend_frame.secondRoll is not None:
                    rolls.append(frontend_frame.secondRoll)
                if frontend_frame.thirdRoll is not None:
                    rolls.append(frontend_frame.thirdRoll)
                
                backend_frame = Frame(
                    number=frontend_frame.frameNumber,
                    rolls=rolls,
                    score=frontend_frame.frameScore or 0,
                    is_strike=frontend_frame.isStrike,
                    is_spare=frontend_frame.isSpare,
                    is_completed=frontend_frame.isCompleted
                )
                backend_frames.append(backend_frame)
            
            # ゲームデータを作成
            game_create_data = GameCreate(
                user_id=user_id,
                total_score=game_data.totalScore,
                frames=backend_frames,
                status="completed",
                played_at=datetime.fromisoformat(game_data.gameDate.replace('Z', '+00:00'))
            )
            
            # ゲーム作成
            game_schema = await self.game_repo.create(game_create_data)
            
            GameLogger.log_game_completed(game_schema.id, user_id, game_data.totalScore)
            
            return GameResponse(
                id=game_schema.id,
                user_id=game_schema.user_id,
                total_score=game_schema.total_score,
                frames=game_schema.frames,
                status=game_schema.status,
                played_at=game_schema.played_at,
                created_at=game_schema.created_at,
                updated_at=game_schema.updated_at
            )
            
        except ValueError as e:
            logger.warning(f"Failed to save completed game: {e}")
            raise
        except Exception as e:
            logger.error(f"Failed to save completed game: {e}")
            raise
