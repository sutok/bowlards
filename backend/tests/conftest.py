"""テスト設定"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch
from app.main import app


@pytest.fixture
def client():
    """テストクライアント"""
    return TestClient(app)


@pytest.fixture
def mock_firestore():
    """Firestoreモック"""
    return Mock()


@pytest.fixture
def mock_firebase_auth():
    """Firebase認証モック"""
    with patch('app.auth.firebase.firebase_auth') as mock:
        yield mock


@pytest.fixture
def sample_user_data():
    """サンプルユーザーデータ"""
    return {
        "uid": "test_user_123",
        "email": "test@example.com",
        "display_name": "Test User",
        "photo_url": "https://example.com/photo.jpg"
    }


@pytest.fixture
def sample_game_data():
    """サンプルゲームデータ"""
    return {
        "id": "test_game_123",
        "user_id": "test_user_123",
        "total_score": 0,
        "status": "playing",
        "frames": []
    }
