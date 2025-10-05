"""ゲームAPIルーター"""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict, Any
from app.auth.dependencies import get_current_user, get_current_user_id
from app.services.game_service import GameService
from app.models.game import GameResponse, RollRequest, GameHistoryRequest, GameHistoryResponse, GameStatistics, CompletedGameRequest
from app.models.common import success_response, error_response, MetaInfo
from app.exceptions import GameNotFoundError, InvalidRollError, GameCompletedError
from app.utils.logging import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/games", tags=["games"])


def get_game_service() -> GameService:
    """ゲームサービスの依存関係注入"""
    from app.dependencies import get_firestore_client
    from app.repositories.game_repository import GameRepository
    from app.repositories.user_repository import UserRepository
    
    db = get_firestore_client()
    game_repo = GameRepository(db)
    user_repo = UserRepository(db)
    return GameService(game_repo, user_repo)


@router.post("/", response_model=Dict[str, Any])
async def save_game(
    game_data: CompletedGameRequest,
    current_user: Dict[str, Any] = Depends(get_current_user),
    game_service: GameService = Depends(get_game_service)
):
    """
    完了したゲームを保存
    
    userIdは認証トークンから自動的に取得されます。
    
    リクエスト例:
    ```json
    {
      "gameDate": "2025-10-05T12:00:00Z",
      "totalScore": 150,
      "frames": [
        {
          "frameNumber": 1,
          "firstRoll": 10,
          "secondRoll": null,
          "thirdRoll": null,
          "frameScore": 20,
          "isStrike": true,
          "isSpare": false,
          "isCompleted": true
        },
        {
          "frameNumber": 2,
          "firstRoll": 7,
          "secondRoll": 3,
          "thirdRoll": null,
          "frameScore": 35,
          "isStrike": false,
          "isSpare": true,
          "isCompleted": true
        }
      ],
      "status": "completed"
    }
    ```
    
    注意: 
    - frameNumberは1から10まで（0始まりではありません）
    - userIdはリクエストに含めないでください（認証トークンから自動取得）
    """
    try:
        uid = current_user.get("uid")
        
        # 認証トークンからuserIdを取得してゲームデータを保存
        game = await game_service.save_completed_game_with_uid(uid, game_data)
        return success_response(data=game.dict())
        
    except ValueError as e:
        return error_response("USER_NOT_FOUND", str(e))
    except Exception as e:
        logger.error(f"Failed to save game: {e}")
        return error_response("SAVE_FAILED", "Failed to save game")


@router.post("/create", response_model=Dict[str, Any])
async def create_game(
    current_user: Dict[str, Any] = Depends(get_current_user),
    game_service: GameService = Depends(get_game_service)
):
    """新しいゲームを作成"""
    try:
        uid = current_user.get("uid")
        game = await game_service.create_game(uid)
        return success_response(data=game.dict())
        
    except ValueError as e:
        return error_response("USER_NOT_FOUND", str(e))
    except Exception as e:
        logger.error(f"Failed to create game: {e}")
        return error_response("CREATE_FAILED", "Failed to create game")


@router.get("/{game_id}", response_model=Dict[str, Any])
async def get_game(
    game_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user),
    game_service: GameService = Depends(get_game_service)
):
    """ゲームを取得"""
    try:
        uid = current_user.get("uid")
        game = await game_service.get_game(game_id, uid)
        return success_response(data=game.dict())
        
    except GameNotFoundError:
        return error_response("GAME_NOT_FOUND", "Game not found")
    except Exception as e:
        logger.error(f"Failed to get game {game_id}: {e}")
        return error_response("GET_FAILED", "Failed to get game")


@router.post("/{game_id}/roll", response_model=Dict[str, Any])
async def add_roll(
    game_id: str,
    roll: RollRequest,
    current_user: Dict[str, Any] = Depends(get_current_user),
    game_service: GameService = Depends(get_game_service)
):
    """ロールを追加"""
    try:
        uid = current_user.get("uid")
        game = await game_service.add_roll(game_id, uid, roll)
        return success_response(data=game.dict())
        
    except GameNotFoundError:
        return error_response("GAME_NOT_FOUND", "Game not found")
    except InvalidRollError as e:
        return error_response("INVALID_ROLL", str(e))
    except GameCompletedError:
        return error_response("GAME_COMPLETED", "Game is already completed")
    except Exception as e:
        logger.error(f"Failed to add roll to game {game_id}: {e}")
        return error_response("UPDATE_FAILED", "Failed to add roll")


@router.delete("/{game_id}", response_model=Dict[str, Any])
async def delete_game(
    game_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user),
    game_service: GameService = Depends(get_game_service)
):
    """ゲームを削除"""
    try:
        uid = current_user.get("uid")
        await game_service.delete_game(game_id, uid)
        return success_response(data={"message": "Game deleted successfully"})
        
    except GameNotFoundError:
        return error_response("GAME_NOT_FOUND", "Game not found")
    except Exception as e:
        logger.error(f"Failed to delete game {game_id}: {e}")
        return error_response("DELETE_FAILED", "Failed to delete game")


@router.get("/history", response_model=Dict[str, Any])
async def get_game_history(
    limit: int = 20,
    offset: int = 0,
    status: str = None,
    current_user: Dict[str, Any] = Depends(get_current_user),
    game_service: GameService = Depends(get_game_service)
):
    """ゲーム履歴を取得"""
    try:
        uid = current_user.get("uid")
        history_request = GameHistoryRequest(
            limit=limit,
            offset=offset,
            status=status
        )
        history = await game_service.get_game_history(uid, history_request)
        
        meta = MetaInfo(
            total=history.total,
            limit=history.limit,
            offset=history.offset
        )
        
        return success_response(
            data=[game.dict() for game in history.games],
            meta=meta
        )
        
    except Exception as e:
        logger.error(f"Failed to get game history: {e}")
        return error_response("GET_FAILED", "Failed to get game history")


@router.get("/statistics", response_model=Dict[str, Any])
async def get_game_statistics(
    current_user: Dict[str, Any] = Depends(get_current_user),
    game_service: GameService = Depends(get_game_service)
):
    """ゲーム統計を取得"""
    try:
        uid = current_user.get("uid")
        stats = await game_service.get_game_statistics(uid)
        return success_response(data=stats.dict())
        
    except Exception as e:
        logger.error(f"Failed to get game statistics: {e}")
        return error_response("GET_FAILED", "Failed to get game statistics")
