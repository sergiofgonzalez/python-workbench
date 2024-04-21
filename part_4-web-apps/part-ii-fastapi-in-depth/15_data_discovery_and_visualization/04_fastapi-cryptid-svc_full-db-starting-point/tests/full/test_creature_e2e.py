"""
End-to-end test for the Creature resource.
"""

from typing import Generator

import pytest
from fastapi import status
from fastapi.testclient import TestClient

from cryptid.main import app
from cryptid.model.creature import Creature

client = TestClient(app)


def _reset_creatures():
    creatures = client.get("/creature").json()
    for creature in creatures:
        client.delete(f"/creature/{creature['name']}")


@pytest.fixture(name="dragon_sample")
def fixture_dragon_sample() -> Generator[Creature, None, None]:
    yield Creature(
        name="Dragon",
        description="A large creature with wings that expels fire",
        country="*",
        area="*",
        aka="firedrake",
    )
    _reset_creatures()  # Clean up


@pytest.fixture(name="yeti_sample")
def fixture_yeti_sample() -> Generator[Creature, None, None]:
    yield Creature(
        name="Yeti",
        description="Hirsute Himalayan",
        country="CN",
        area="Himalayas",
        aka="Abominable Snowman",
    )
    _reset_creatures()  # Clean up


def test_create(dragon_sample: Creature):
    response = client.post("/creature", json=dragon_sample.model_dump())
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == dragon_sample.model_dump()


def test_create_duplicate(dragon_sample: Creature):
    client.post("/creature", json=dragon_sample.model_dump())
    response = client.post("/creature", json=dragon_sample.model_dump())
    assert response.status_code == status.HTTP_409_CONFLICT
    assert "exists" in response.json()["detail"].lower()
    assert "creature" in response.json()["detail"].lower()
    assert dragon_sample.name in response.json()["detail"]


def test_get_one(dragon_sample: Creature):
    client.post("/creature", json=dragon_sample.model_dump())
    response = client.get(f"/creature/{dragon_sample.name}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == dragon_sample.model_dump()


def test_get_one_missing():
    response = client.get("/creature/nonexistent")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "not found" in response.json()["detail"].lower()
    assert "creature" in response.json()["detail"].lower()
    assert "nonexistent" in response.json()["detail"].lower()


def test_get_all_several(dragon_sample: Creature, yeti_sample: Creature):
    client.post("/creature", json=dragon_sample.model_dump())
    client.post("/creature", json=yeti_sample.model_dump())
    response = client.get("/creature")
    assert response.status_code == status.HTTP_200_OK

    # The order of the returned creatures is not guaranteed
    assert dragon_sample.model_dump() in response.json()
    assert yeti_sample.model_dump() in response.json()
    assert len(response.json()) == 2

def test_get_all_empty():
    response = client.get("/creature")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []

def test_get_all_one(dragon_sample: Creature):
    client.post("/creature", json=dragon_sample.model_dump())
    response = client.get("/creature")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [dragon_sample.model_dump()]


def test_patch(dragon_sample: Creature):
    client.post("/creature", json=dragon_sample.model_dump())
    response = client.patch(
        f"/creature/{dragon_sample.name}",
        json={
            "name": "mod_creature",
            "description": "A modified creature",
            "country": "MC",
            "area": "MA",
            "aka": "modaka",
        },
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "name": "mod_creature",
        "description": "A modified creature",
        "country": "MC",
        "area": "MA",
        "aka": "modaka",
    }
    assert (
        client.get(f"/creature/{dragon_sample.name}").status_code
        == status.HTTP_404_NOT_FOUND
    )
    assert client.get("/creature/mod_creature").json() == {
        "name": "mod_creature",
        "description": "A modified creature",
        "country": "MC",
        "area": "MA",
        "aka": "modaka",
    }


def test_patch_missing():
    response = client.patch(
        "/creature/nonexistent",
        json={
            "name": "mod_creature",
            "description": "A modified creature",
            "country": "MC",
            "area": "MA",
            "aka": "modaka",
        },
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "not found" in response.json()["detail"].lower()
    assert "creature" in response.json()["detail"].lower()
    assert "nonexistent" in response.json()["detail"].lower()


def test_patch_duplicate(dragon_sample: Creature, yeti_sample: Creature):
    client.post("/creature", json=dragon_sample.model_dump())
    client.post("/creature", json=yeti_sample.model_dump())
    response = client.patch(
        f"/creature/{dragon_sample.name}",
        json={
            "name": yeti_sample.name,
        },
    )
    assert response.status_code == status.HTTP_409_CONFLICT
    assert "exists" in response.json()["detail"].lower()
    assert "creature" in response.json()["detail"].lower()
    assert yeti_sample.name in response.json()["detail"]


def test_put(dragon_sample: Creature, yeti_sample: Creature):
    client.post("/creature", json=dragon_sample.model_dump())
    response = client.put(
        f"/creature/{dragon_sample.name}", json=yeti_sample.model_dump()
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == yeti_sample.model_dump()
    assert (
        client.get(f"/creature/{dragon_sample.name}").status_code
        == status.HTTP_404_NOT_FOUND
    )


def test_put_missing(dragon_sample: Creature):
    response = client.put(
        "/creature/nonexistent", json=dragon_sample.model_dump()
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "not found" in response.json()["detail"].lower()
    assert "creature" in response.json()["detail"].lower()
    assert "nonexistent" in response.json()["detail"].lower()


def test_put_duplicate(dragon_sample: Creature, yeti_sample: Creature):
    client.post("/creature", json=dragon_sample.model_dump())
    client.post("/creature", json=yeti_sample.model_dump())
    response = client.put(
        f"/creature/{dragon_sample.name}", json=yeti_sample.model_dump()
    )
    assert response.status_code == status.HTTP_409_CONFLICT
    assert "exists" in response.json()["detail"].lower()
    assert "creature" in response.json()["detail"].lower()
    assert yeti_sample.name in response.json()["detail"]


def test_delete(dragon_sample: Creature):
    client.post("/creature", json=dragon_sample.model_dump())
    response = client.delete(f"/creature/{dragon_sample.name}")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert (
        client.get(f"/creature/{dragon_sample.name}").status_code
        == status.HTTP_404_NOT_FOUND
    )


def test_delete_missing():
    response = client.delete("/creature/nonexistent")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "not found" in response.json()["detail"].lower()
    assert "creature" in response.json()["detail"].lower()
    assert "nonexistent" in response.json()["detail"].lower()
