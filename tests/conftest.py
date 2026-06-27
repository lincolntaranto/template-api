import pytest
from sqlalchemy import delete, create_engine
from sqlalchemy.orm import Session
from starlette.testclient import TestClient

from core.config import settings
from core.limiter import limiter
from main import app
from models import User
from models.base import Base
from models.session import get_session
from unittest.mock import patch

test_engine = create_engine(settings.DATABASE_TEST_URL)

USER_DATA = {"name": "Teste", "email": "pyteste@email.com", "password": "123"}
USER_DATA_WRONG = {"name": "Teste2", "email": "pytesteemail.com", "password": "123"}


def override_get_session():
    with Session(test_engine) as session:
        yield session


@pytest.fixture(scope="session", autouse=True)
def criar_tabelas():
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture(scope="session")
def client():
    app.dependency_overrides[get_session] = override_get_session
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture(autouse=True)
def disable_limiter():
    limiter.enabled = False
    yield
    limiter.enabled = True


@pytest.fixture(autouse=True)
def limpar_banco():
    yield
    with Session(test_engine) as session:
        session.execute(delete(User))
        session.commit()


@pytest.fixture()
def token(client):
    client.post("/auth/create_user", json=USER_DATA)
    response = client.post(
        "/auth/login",
        json={"email": USER_DATA["email"], "password": USER_DATA["password"]},
    )
    return response.json()["access_token"]


@pytest.fixture(autouse=True)
def mock_send_email():
    with patch("core.email.utils.send_email") as mock:
        yield mock
