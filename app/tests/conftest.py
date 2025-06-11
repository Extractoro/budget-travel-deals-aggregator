import pytest
from pathlib import Path
from fastapi.testclient import TestClient
from app.main import app
from dotenv import load_dotenv

dotenv_path = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(dotenv_path=dotenv_path)


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def auth_token(client):
    data = {"username": "user123", "password": "qwerty123"}
    client.post("/auth/signup", json=data)
    response = client.post("/auth/login", json=data)
    return response.json()["access_token"]
