from tests.conftest import USER_DATA

CHANGE_PASSWORD = {"current_password": USER_DATA["password"], "new_password": "1234"}
CHANGE_PASSWORD_EQUAL = {
    "current_password": USER_DATA["password"],
    "new_password": "123",
}
CHANGE_EMAIL = {
    "new_email": "novoemail@gmail.com",
    "current_password": USER_DATA["password"],
}
CHANGE_EMAIL_EQUAL = {
    "new_email": USER_DATA["email"],
    "current_password": USER_DATA["password"],
}
CHANGE_EMAIL_WRONG_PASSWORD = {
    "new_email": USER_DATA["email"],
    "current_password": "wrongPassword",
}
CHANGE_USERNAME = {
    "new_name": "Novo nome",
    "current_password": USER_DATA["password"],
}
CHANGE_USERNAME_WRONG_PASSWORD = {
    "new_name": "Novo nome",
    "current_password": "wrongPassword",
}


def test_change_password(token, client):
    response = client.patch(
        "/user/password",
        json=CHANGE_PASSWORD,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200


def test_change_password_equal(token, client):
    response = client.patch(
        "/user/password",
        json=CHANGE_PASSWORD_EQUAL,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 400


def test_change_email(token, client):
    response = client.patch(
        "/user/email",
        json=CHANGE_EMAIL,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200


def test_change_email_equal(token, client):
    response = client.patch(
        "/user/email",
        json=CHANGE_EMAIL_EQUAL,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 400


def test_change_email_wrong_password(token, client):
    response = client.patch(
        "/user/email",
        json=CHANGE_EMAIL_WRONG_PASSWORD,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 401


def test_change_username(token, client):
    response = client.patch(
        "/user/username",
        json=CHANGE_USERNAME,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200


def test_change_username_wrong_password(token, client):
    response = client.patch(
        "/user/username",
        json=CHANGE_USERNAME_WRONG_PASSWORD,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 401


def test_delete_account(token, client):
    response = client.request(
        "DELETE",
        "/user/",
        json={"current_password": USER_DATA["password"]},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200


def test_delete_account_wrong_password(token, client):
    response = client.request(
        "DELETE",
        "/user/",
        json={"current_password": "wrongPassword"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 401
