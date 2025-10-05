"""依存関係注入"""
from google.cloud import firestore
from firebase_admin import firestore as admin_firestore
from app.repositories.user_repository import UserRepository
from app.repositories.game_repository import GameRepository
from app.services.user_service import UserService
from app.services.game_service import GameService


def get_firestore_client() -> firestore.Client:
    """Firestoreクライアントを取得（Firebase Admin SDK経由）"""
    return admin_firestore.client()


def get_user_repository(db: firestore.Client = None) -> UserRepository:
    """ユーザーリポジトリを取得"""
    if db is None:
        db = get_firestore_client()
    return UserRepository(db)


def get_game_repository(db: firestore.Client = None) -> GameRepository:
    """ゲームリポジトリを取得"""
    if db is None:
        db = get_firestore_client()
    return GameRepository(db)


def get_user_service(user_repo: UserRepository = None) -> UserService:
    """ユーザーサービスを取得"""
    if user_repo is None:
        user_repo = get_user_repository()
    return UserService(user_repo)


def get_game_service(game_repo: GameRepository = None, user_repo: UserRepository = None) -> GameService:
    """ゲームサービスを取得"""
    if game_repo is None:
        game_repo = get_game_repository()
    if user_repo is None:
        user_repo = get_user_repository()
    return GameService(game_repo, user_repo)
