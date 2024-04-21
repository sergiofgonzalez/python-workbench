"""
End-to-end test for the User resource.
"""

from typing import Generator

import pytest
from fastapi import status
from fastapi.testclient import TestClient

from cryptid.data import user as data
from cryptid.data.init import curs
from cryptid.main import app
from cryptid.model.user import User
from cryptid.service import user as service

client = TestClient(app)


def _reset_users():
    if curs:
        curs.execute("DROP TABLE IF EXISTS user")
        curs.execute("DROP TABLE IF EXISTS xuser")
        data._init_table()  # pylint: disable=W0212:protected-access


@pytest.fixture(name="user1_sample")
def fixture_user1_sample() -> Generator[User, None, None]:
    yield User(name="user1", password_hash="hash1")
    _reset_users()  # Clean up


@pytest.fixture(name="user2_sample")
def fixture_user2_sample() -> Generator[User, None, None]:
    yield User(name="user2", password_hash="hash2")
    _reset_users()  # Clean up


def test_create(user1_sample: User):
    response = client.post("/user", json=user1_sample.model_dump())
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == user1_sample.model_dump()


def test_create_duplicate(user1_sample: User):
    client.post("/user", json=user1_sample.model_dump())
    response = client.post("/user", json=user1_sample.model_dump())
    assert response.status_code == status.HTTP_409_CONFLICT
    assert "exists" in response.json()["detail"].lower()
    assert "user" in response.json()["detail"].lower()
    assert user1_sample.name in response.json()["detail"]


def test_get_one(user1_sample: User):
    client.post("/user", json=user1_sample.model_dump())
    response = client.get(f"/user/{user1_sample.name}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == user1_sample.model_dump()


def test_get_one_missing():
    response = client.get("/user/missing")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "missing" in response.json()["detail"].lower()
    assert "user" in response.json()["detail"].lower()


def test_get_all_several(user1_sample: User, user2_sample: User):
    client.post("/user", json=user1_sample.model_dump())
    client.post("/user", json=user2_sample.model_dump())
    response = client.get("/user")
    assert response.status_code == status.HTTP_200_OK
    # The order of the returned list is not guaranteed
    assert user1_sample.model_dump() in response.json()
    assert user2_sample.model_dump() in response.json()
    assert len(response.json()) == 2


def test_get_all_one(user1_sample: User):
    client.post("/user", json=user1_sample.model_dump())
    response = client.get("/user")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [user1_sample.model_dump()]


def test_get_all_empty():
    response = client.get("/user")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []


def test_patch(user1_sample: User):
    client.post("/user", json=user1_sample.model_dump())
    response = client.patch(
        f"/user/{user1_sample.name}",
        json={"password_hash": "new_hash"},
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["password_hash"] == "new_hash"
    assert response.json()["name"] == user1_sample.name


def test_patch_missing():
    response = client.patch(
        "/user/missing",
        json={"password_hash": "new_hash"},
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "missing" in response.json()["detail"].lower()
    assert "user" in response.json()["detail"].lower()


def test_patch_duplicate(user1_sample: User, user2_sample: User):
    client.post("/user", json=user1_sample.model_dump())
    client.post("/user", json=user2_sample.model_dump())
    response = client.patch(
        f"/user/{user1_sample.name}",
        json=user2_sample.model_dump(),
    )
    assert response.status_code == status.HTTP_409_CONFLICT
    assert "exists" in response.json()["detail"].lower()
    assert "user" in response.json()["detail"].lower()
    assert user2_sample.name in response.json()["detail"]


def test_put(user1_sample: User, user2_sample: User):
    client.post("/user", json=user1_sample.model_dump())
    response = client.put(
        f"/user/{user1_sample.name}",
        json=user2_sample.model_dump(),
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == user2_sample.model_dump()
    assert (
        client.get(f"/user/{user1_sample.name}").status_code
        == status.HTTP_404_NOT_FOUND
    )


def test_put_missing(user1_sample: User):
    response = client.put(
        "/user/missing",
        json=user1_sample.model_dump(),
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "missing" in response.json()["detail"].lower()
    assert "user" in response.json()["detail"].lower()


def test_put_duplicate(user1_sample: User, user2_sample: User):
    client.post("/user", json=user1_sample.model_dump())
    client.post("/user", json=user2_sample.model_dump())
    response = client.put(
        f"/user/{user1_sample.name}",
        json=user2_sample.model_dump(),
    )
    assert response.status_code == status.HTTP_409_CONFLICT
    assert "exists" in response.json()["detail"].lower()
    assert "user" in response.json()["detail"].lower()
    assert user2_sample.name in response.json()["detail"]


def test_delete(user1_sample: User):
    client.post("/user", json=user1_sample.model_dump())
    response = client.delete(f"/user/{user1_sample.name}")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert (
        client.get(f"/user/{user1_sample.name}").status_code
        == status.HTTP_404_NOT_FOUND
    )


def test_delete_missing():
    response = client.delete("/user/missing")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "missing" in response.json()["detail"].lower()
    assert "user" in response.json()["detail"].lower()
    assert "missing" in response.json()["detail"].lower()


def test_post_token_unknown_user():
    # Tries to authenticate the user with via a user/password form
    response = client.post(
        "/user/token",
        data={
            "username": "user1",
            "password": "hash1",
        },
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Incorrect username or password"
    assert response.headers.get("www-authenticate") == "Bearer"


def test_create_user_real_hash(user1_sample: User):
    # get the hash of the password
    plain_text_password = "fidelio"
    user1_sample.password_hash = service.get_hash(plain_text_password)

    # create the user
    response = client.post("/user", json=user1_sample.model_dump())
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == user1_sample.model_dump()

    # authenticate the user
    response = client.post(
        "/user/token",
        data={
            "username": user1_sample.name,
            "password": plain_text_password,
        },
    )
    assert response.status_code == status.HTTP_200_OK
    assert "access_token" in response.json()
    assert "token_type" in response.json()
    assert response.json()["token_type"] == "bearer"
    access_token = response.json()["access_token"]

    # invoke a protected endpoint
    response = client.get(
        "/user/token",
        headers={"Authorization": f"Bearer {response.json()['access_token']}"},
    )
    assert response.status_code == status.HTTP_200_OK
    assert "token" in response.json()
    assert response.json()["token"] == access_token
