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
