import pytest
from sqlalchemy import delete, create_engine
from sqlalchemy.orm import Session
from starlette.testclient import TestClient
from testcontainers.postgres import PostgresContainer

from core.limiter import limiter
from main import app
from models import User
from models.base import Base
from models.session import get_session
from unittest.mock import patch

USER_DATA = {"name": "Teste", "email": "pyteste@email.com", "password": "123"}
USER_DATA_WRONG = {"name": "Teste2", "email": "pytesteemail.com", "password": "123"}


@pytest.fixture(scope="session")
def postgres_container():
    with PostgresContainer("postgres:17", driver="psycopg2") as postgres:
        yield postgres


@pytest.fixture(scope="session")
def test_engine(postgres_container):
    engine = create_engine(postgres_container.get_connection_url())
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)
    engine.dispose()


@pytest.fixture(scope="session")
def client(test_engine):
    def override_get_session():
        with Session(test_engine) as session:
            yield session

    app.dependency_overrides[get_session] = override_get_session
    with TestClient(app, base_url="http://testserver/api/v1") as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture(autouse=True)
def disable_limiter():
    limiter.enabled = False
    yield
    limiter.enabled = True


@pytest.fixture(autouse=True)
def clear_database(test_engine):
    yield
    with Session(test_engine) as session:
        session.execute(delete(User))
        session.commit()


@pytest.fixture()
def token(client):
    client.post("/auth/user", json=USER_DATA)
    response = client.post(
        "/auth/login",
        json={"email": USER_DATA["email"], "password": USER_DATA["password"]},
    )
    return response.json()["access_token"]


@pytest.fixture(autouse=True)
def mock_send_email():
    with patch("routes.auth_routes.send_email"), patch("routes.user_routes.send_email"):
        yield
