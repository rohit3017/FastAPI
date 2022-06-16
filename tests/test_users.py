from types import new_class
from app import schemas
from jose import jwt
from app.config import settings
import pytest


def test_root(client):
    res = client.get("/")
    assert res.json().get("message") == "hello fastapi"
    assert res.status_code == 200


def test_create_user(client):
    res = client.post(
        "/users/", json={"email": "hello@gmail.com", "password": "password123"}
    )
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "hello@gmail.com"
    assert res.status_code == 201


def test_login(client, test_user):
    res = client.post(
        "/login",
        data={"username": test_user["email"], "password": test_user["password"]},
    )
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(
        login_res.access_token, settings.secret_key, algorithms=[settings.algoritham]
    )
    id = payload.get("user_id")
    assert id == test_user["id"]
    assert login_res.token_type == "Bearer"
    assert res.status_code == 200


@pytest.mark.parametrize(
    "username,password,res_code",
    [
        ("rohit@gmail.com", "wrongPassword", 403),
        ("wrongUsername", "password123", 403),
        ("wrongusername", "wrongpassword", 403),
        (None, "password123", 422),
        ("rohit@gmail.com", None, 422),
    ],
)
def test_failed_login(client, test_user, username, password, res_code):
    res = client.post("/login", data={"username": username, "password": password})
    assert res.status_code == res_code
