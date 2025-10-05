"""メインアプリケーションのテスト"""
import pytest
from fastapi.testclient import TestClient


def test_root_endpoint(client: TestClient):
    """ルートエンドポイントのテスト"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["message"] == "Scoring Bowlards API"


def test_health_check(client: TestClient):
    """ヘルスチェックのテスト"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["status"] == "healthy"


def test_docs_endpoint(client: TestClient):
    """Swagger UIエンドポイントのテスト"""
    response = client.get("/docs")
    assert response.status_code == 200


def test_redoc_endpoint(client: TestClient):
    """ReDocエンドポイントのテスト"""
    response = client.get("/redoc")
    assert response.status_code == 200
