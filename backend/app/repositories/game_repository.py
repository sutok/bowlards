"""ゲームリポジトリ"""
from google.cloud import firestore
from typing import List, Optional
from datetime import datetime, timedelta
import logging
from app.models.game import GameSchema, GameCreate, GameHistoryRequest, GameHistoryResponse
from app.exceptions import GameNotFoundError

logger = logging.getLogger(__name__)


class GameRepository:
    """ゲームリポジトリ"""
    
    def __init__(self, db: firestore.Client):
        self.db = db
        self.collection = "games"
    
    async def create(self, game_data: GameCreate) -> GameSchema:
        """ゲームを作成"""
        try:
            doc_ref = self.db.collection(self.collection).document()
            
            # TTL設定（3ヶ月後）
            expire_at = datetime.now() + timedelta(days=90)
            
            game_dict = game_data.dict()
            game_dict['id'] = doc_ref.id
            game_dict['created_at'] = firestore.SERVER_TIMESTAMP
            game_dict['updated_at'] = firestore.SERVER_TIMESTAMP
            game_dict['expire_at'] = expire_at
            
            doc_ref.set(game_dict)
            
            # 作成されたゲームを取得
            doc = doc_ref.get()
            game_data_dict = doc.to_dict()
            game_data_dict['id'] = doc.id
            
            logger.info(f"Game created: {doc_ref.id}")
            return GameSchema(**game_data_dict)
            
        except Exception as e:
            logger.error(f"Failed to create game: {e}")
            raise
    
    async def get_by_id(self, game_id: str, user_id: str) -> Optional[GameSchema]:
        """ゲームIDでゲームを取得"""
        try:
            doc = self.db.collection(self.collection).document(game_id).get()
            
            if not doc.exists:
                return None
            
            game_data = doc.to_dict()
            
            # ユーザー権限チェック
            if game_data.get('user_id') != user_id:
                return None
            
            game_data['id'] = doc.id
            return GameSchema(**game_data)
            
        except Exception as e:
            logger.error(f"Failed to get game {game_id}: {e}")
            raise
    
    async def update(self, game_id: str, game_data: GameSchema) -> GameSchema:
        """ゲームを更新"""
        try:
            doc_ref = self.db.collection(self.collection).document(game_id)
            
            # 既存チェック
            if not doc_ref.get().exists:
                raise GameNotFoundError()
            
            update_data = game_data.dict(exclude={'id', 'created_at'})
            update_data['updated_at'] = firestore.SERVER_TIMESTAMP
            
            doc_ref.update(update_data)
            
            # 更新されたゲームを取得
            doc = doc_ref.get()
            game_data_dict = doc.to_dict()
            game_data_dict['id'] = doc.id
            
            logger.info(f"Game updated: {game_id}")
            return GameSchema(**game_data_dict)
            
        except GameNotFoundError:
            raise
        except Exception as e:
            logger.error(f"Failed to update game {game_id}: {e}")
            raise
    
    async def delete(self, game_id: str, user_id: str) -> bool:
        """ゲームを削除"""
        try:
            doc_ref = self.db.collection(self.collection).document(game_id)
            doc = doc_ref.get()
            
            if not doc.exists:
                raise GameNotFoundError()
            
            game_data = doc.to_dict()
            
            # ユーザー権限チェック
            if game_data.get('user_id') != user_id:
                raise GameNotFoundError()
            
            doc_ref.delete()
            
            logger.info(f"Game deleted: {game_id}")
            return True
            
        except GameNotFoundError:
            raise
        except Exception as e:
            logger.error(f"Failed to delete game {game_id}: {e}")
            raise
    
    async def get_user_games(
        self, 
        user_id: str, 
        history_request: GameHistoryRequest
    ) -> GameHistoryResponse:
        """ユーザーのゲーム履歴を取得"""
        try:
            logger.info(f"🔍 Searching games for user_id: {user_id}")
            logger.info(f"   Collection: {self.collection}")
            logger.info(f"   Limit: {history_request.limit}, Offset: {history_request.offset}")
            logger.info(f"   Status filter: {history_request.status}")
            
            # user_idで検索
            query = self.db.collection(self.collection).where(
                field_path="user_id",
                op_string="==",
                value=user_id
            )
            
            # ステータスフィルター
            if history_request.status:
                query = query.where(
                    field_path="status",
                    op_string="==",
                    value=history_request.status
                )
            
            # デバッグ: 全ゲームドキュメントを確認
            all_docs = list(self.db.collection(self.collection).stream())
            logger.info(f"📚 Total games in collection: {len(all_docs)}")
            if all_docs:
                sample_game = all_docs[0].to_dict()
                logger.info(f"   Sample game data: {{'user_id': '{sample_game.get('user_id')}', 'status': '{sample_game.get('status')}'}}")
            
            # 総件数を取得
            total_query = query
            total_docs = list(total_query.stream())
            total = len(total_docs)
            
            logger.info(f"   Found {total} games matching user_id: {user_id}")
            
            # ページネーション
            query = query.order_by("played_at", direction=firestore.Query.DESCENDING)
            query = query.limit(history_request.limit).offset(history_request.offset)
            
            docs = query.stream()
            games = []
            
            for doc in docs:
                game_data = doc.to_dict()
                game_data['id'] = doc.id
                games.append(GameSchema(**game_data))
            
            logger.info(f"✅ Retrieved {len(games)} games for user {user_id} (total: {total})")
            return GameHistoryResponse(
                games=games,
                total=total,
                limit=history_request.limit,
                offset=history_request.offset
            )
            
        except Exception as e:
            logger.error(f"❌ Failed to get user games for {user_id}: {e}", exc_info=True)
            raise
    
    async def get_user_statistics(self, user_id: str) -> dict:
        """ユーザーのゲーム統計を取得"""
        try:
            logger.info(f"📊 Getting statistics for user_id: {user_id}")
            
            # 完了したゲームのみを取得
            query = self.db.collection(self.collection).where(
                field_path="user_id",
                op_string="==",
                value=user_id
            ).where(
                field_path="status",
                op_string="==",
                value="completed"
            )
            docs = list(query.stream())
            
            logger.info(f"   Found {len(docs)} completed games")
            
            if not docs:
                return {
                    "total_games": 0,
                    "completed_games": 0,
                    "average_score": 0.0,
                    "highest_score": 0,
                    "lowest_score": 0,
                    "strike_count": 0,
                    "spare_count": 0,
                    "perfect_games": 0,
                    "turkey_count": 0
                }
            
            total_games = len(docs)
            completed_games = len(docs)
            scores = [doc.to_dict().get('total_score', 0) for doc in docs]
            
            # 統計計算
            average_score = sum(scores) / len(scores) if scores else 0.0
            highest_score = max(scores) if scores else 0
            lowest_score = min(scores) if scores else 0
            perfect_games = sum(1 for score in scores if score == 300)
            
            # ストライク・スペア・ターキーカウント
            strike_count = 0
            spare_count = 0
            turkey_count = 0
            
            for doc in docs:
                game_data = doc.to_dict()
                frames = game_data.get('frames', [])
                
                for frame in frames:
                    if frame.get('is_strike'):
                        strike_count += 1
                    if frame.get('is_spare'):
                        spare_count += 1
                
                # ターキーカウント（3連続ストライク）
                consecutive_strikes = 0
                for frame in frames:
                    if frame.get('is_strike'):
                        consecutive_strikes += 1
                        if consecutive_strikes >= 3:
                            turkey_count += 1
                    else:
                        consecutive_strikes = 0
            
            statistics = {
                "total_games": total_games,
                "completed_games": completed_games,
                "average_score": round(average_score, 1),
                "highest_score": highest_score,
                "lowest_score": lowest_score,
                "strike_count": strike_count,
                "spare_count": spare_count,
                "perfect_games": perfect_games,
                "turkey_count": turkey_count
            }
            
            logger.info(f"Retrieved statistics for user {user_id}")
            return statistics
            
        except Exception as e:
            logger.error(f"Failed to get user statistics for {user_id}: {e}")
            raise
