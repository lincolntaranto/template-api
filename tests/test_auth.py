from core.security import generate_password_reset_token

USER_DATA = {"name": "Teste", "email": "pyteste@email.com", "password": "123"}
USER_DATA_WRONG = {"name": "Teste2", "email": "pytesteemail.com", "password": "123"}


def test_create_user(client):
    response = client.post("/auth/create_user", json=USER_DATA)
    assert response.status_code == 200


def test_create_user_duplicate_email(client):
    client.post("/auth/create_user", json=USER_DATA)
    response = client.post("/auth/create_user", json=USER_DATA)
    assert response.status_code == 400


def test_create_user_wrong_format_email(client):
    response = client.post("/auth/create_user", json=USER_DATA_WRONG)
    assert response.status_code == 422


def test_login_success(client):
    client.post("/auth/create_user", json=USER_DATA)
    response = client.post(
        "/auth/login",
        json={"email": USER_DATA["email"], "password": USER_DATA["password"]},
    )
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_reset_password(client):
    client.post("/auth/create_user", json=USER_DATA)
    password_reset_token = generate_password_reset_token(email=USER_DATA["email"])
    response = client.post(
        "/auth/reset-password/",
        json={"token": password_reset_token, "new_password": "1234"},
    )
    assert response.status_code == 200


def test_reset_password_invalid_token(client):
    client.post("/auth/create_user", json=USER_DATA)
    fake_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjEwLCJuYmYiOjEwLCJzdWIiOiJ3cm9uZ2VtYWlsQGVtYWlsLmNvbSJ9.W0T4sdiUlUd_ON0VAOHJ_Djtg0v3C-MbeR41eBL8ktw"
    response = client.post(
        "/auth/reset-password/", json={"token": fake_token, "new_password": "1234"}
    )
    assert response.status_code == 400
