import pytest
from fastapi.testclient import TestClient
from sqlalchemy import delete
from sqlalchemy.orm import Session

from core.limiter import limiter
from main import app
from models import User
from models.base import db

limiter.enabled = False

client = TestClient(app)

USER_DATA = {
    "name": "Teste",
    "email": "pyteste@email.com",
    "password": "123"
}

USER_DATA_WRONG = {
    "name": "Teste2",
    "email": "pytesteemail.com",
    "password": "123"
}

@pytest.fixture(autouse=True)
def limpar_banco():
    yield
    with Session(db) as session:
        session.execute(delete(User))
        session.commit()

def test_create_user():
    response = client.post("/auth/create_user", json=USER_DATA)
    assert response.status_code == 200

def test_create_user_duplicate_email():
    client.post("/auth/create_user", json=USER_DATA)
    response = client.post("/auth/create_user", json=USER_DATA)
    assert response.status_code == 400

def test_create_user_wrong_format_email():
    response = client.post("/auth/create_user", json=USER_DATA_WRONG)
    assert response.status_code == 422

def teste_login_success():
    response = client.post("/auth/create_user", json=USER_DATA)
    response = client.post("/auth/login", json={
        "email": USER_DATA["email"],
        "password": USER_DATA["password"]
    })
    assert response.status_code == 200
    assert "access_token" in response.json()