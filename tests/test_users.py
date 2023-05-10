import pytest
from app import schemas
from jose import jwt
from app.config import settings


@pytest.fixture
def test_user(client):
    user_data = {"email": "aman@gmail.com",
                 "password": "aman", "phone_number": "7878787878"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user


def test_root(client):
    res = client.get("/")
    print(res.json().get('message'))
    assert res.json().get('message') == "Welcome to Python Tutorial"
    assert res.status_code == 200


def test_create_user(client):
    res = client.post(
        "/users/", json={"email": "aman@gmail.com", "password": "aman", "phone_number": "1231231231"})

    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "aman@gmail.com"
    assert res.status_code == 201


def test_login_user(test_user, client):
    res = client.post(
        "/login", data={"username": test_user['email'], "password": test_user['password']})
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token,
                         settings.secret_key, algorithms=[settings.algorithm])
    id = payload.get("user_id")
    assert id == test_user['id']
    assert login_res.token_type == "Bearer"
    assert res.status_code == 200


def test_incorrect_login(test_user, client):
    res = client.post(
        "/login", data={"username": test_user['email'], "password": "aaaa"})

    assert res.status_code == 403
    assert res.json().get('detail') == 'Invalid Credentials'
