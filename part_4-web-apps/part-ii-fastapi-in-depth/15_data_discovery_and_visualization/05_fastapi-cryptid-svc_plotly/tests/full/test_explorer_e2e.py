"""
End-to-end test for the Creature resource.
"""

from typing import Generator

import pytest
from fastapi import status
from fastapi.testclient import TestClient

from cryptid.main import app
from cryptid.model.explorer import Explorer

client = TestClient(app)


def _reset_explorers():
    explorers = client.get("/explorer").json()
    for explorer in explorers:
        client.delete(f"/explorer/{explorer['name']}")


@pytest.fixture(name="van_helsing_sample")
def fixture_van_helsing_sample() -> Generator[Explorer, None, None]:
    yield Explorer(
        name="Van Helsing",
        country="NL",
        description="Vampire slayer",
    )
    _reset_explorers()  # Clean up


@pytest.fixture(name="guillermo_sample")
def fixture_guillermo_sample() -> Generator[Explorer, None, None]:
    yield Explorer(
        name="Guillermo de la Cruz",
        description="Vampire familiar",
        country="MX",
    )
    _reset_explorers()  # Clean up


def test_create(van_helsing_sample: Explorer):
    response = client.post("/explorer", json=van_helsing_sample.model_dump())
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == van_helsing_sample.model_dump()


def test_create_duplicate(van_helsing_sample: Explorer):
    client.post("/explorer", json=van_helsing_sample.model_dump())
    response = client.post("/explorer", json=van_helsing_sample.model_dump())
    assert response.status_code == status.HTTP_409_CONFLICT
    assert "exists" in response.json()["detail"].lower()
    assert "explorer" in response.json()["detail"].lower()
    assert van_helsing_sample.name in response.json()["detail"]


def test_get_one(van_helsing_sample: Explorer):
    client.post("/explorer", json=van_helsing_sample.model_dump())
    response = client.get(f"/explorer/{van_helsing_sample.name}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == van_helsing_sample.model_dump()


def test_get_one_missing():
    response = client.get("/explorer/nonexistent")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "not found" in response.json()["detail"].lower()
    assert "explorer" in response.json()["detail"].lower()
    assert "nonexistent" in response.json()["detail"]


def test_get_all_several(
    van_helsing_sample: Explorer, guillermo_sample: Explorer
):
    client.post("/explorer", json=van_helsing_sample.model_dump())
    client.post("/explorer", json=guillermo_sample.model_dump())
    response = client.get("/explorer")
    assert response.status_code == status.HTTP_200_OK

    # The order of the returned explorers is not guaranteed
    assert van_helsing_sample.model_dump() in response.json()
    assert guillermo_sample.model_dump() in response.json()


def test_get_all_one(van_helsing_sample: Explorer):
    client.post("/explorer", json=van_helsing_sample.model_dump())
    response = client.get(f"/explorer/{van_helsing_sample.name}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == van_helsing_sample.model_dump()


def test_get_all_empty():
    response = client.get("/explorer")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []


def test_patch(van_helsing_sample: Explorer, guillermo_sample: Explorer):
    client.post("/explorer", json=van_helsing_sample.model_dump())
    response = client.patch(
        f"/explorer/{van_helsing_sample.name}",
        json=guillermo_sample.model_dump(),
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == guillermo_sample.model_dump()

    assert (
        client.get(f"/explorer/{guillermo_sample.name}").json()
        == guillermo_sample.model_dump()
    )

    # The original explorer is gone
    assert (
        client.get(f"/explorer/{van_helsing_sample.name}").status_code
        == status.HTTP_404_NOT_FOUND
    )


def test_patch_missing():
    response = client.patch(
        "/explorer/nonexistent",
        json={"name": "mod_explorer"},
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "not found" in response.json()["detail"].lower()
    assert "explorer" in response.json()["detail"].lower()
    assert "nonexistent" in response.json()["detail"].lower()


def test_patch_duplicate(
    van_helsing_sample: Explorer, guillermo_sample: Explorer
):
    client.post("/explorer", json=van_helsing_sample.model_dump())
    client.post("/explorer", json=guillermo_sample.model_dump())
    response = client.patch(
        f"/explorer/{van_helsing_sample.name}",
        json={"name": guillermo_sample.name},
    )
    assert response.status_code == status.HTTP_409_CONFLICT
    assert "exists" in response.json()["detail"].lower()
    assert "explorer" in response.json()["detail"].lower()
    assert guillermo_sample.name in response.json()["detail"]


def test_put(van_helsing_sample: Explorer, guillermo_sample: Explorer):
    client.post("/explorer", json=van_helsing_sample.model_dump())
    response = client.put(
        f"/explorer/{van_helsing_sample.name}",
        json=guillermo_sample.model_dump(),
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == guillermo_sample.model_dump()
    assert (
        client.get(f"/explorer/{van_helsing_sample.name}").status_code
        == status.HTTP_404_NOT_FOUND
    )


def test_put_missing(van_helsing_sample: Explorer):
    response = client.put(
        "/explorer/nonexistent",
        json=van_helsing_sample.model_dump(),
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "not found" in response.json()["detail"].lower()
    assert "explorer" in response.json()["detail"].lower()
    assert "nonexistent" in response.json()["detail"].lower()


def test_put_duplicate(
    van_helsing_sample: Explorer, guillermo_sample: Explorer
):
    client.post("/explorer", json=van_helsing_sample.model_dump())
    client.post("/explorer", json=guillermo_sample.model_dump())
    response = client.put(
        f"/explorer/{van_helsing_sample.name}",
        json=guillermo_sample.model_dump(),
    )
    assert response.status_code == status.HTTP_409_CONFLICT
    assert "exists" in response.json()["detail"].lower()
    assert "explorer" in response.json()["detail"].lower()
    assert guillermo_sample.name in response.json()["detail"]


def test_delete(van_helsing_sample: Explorer):
    client.post("/explorer", json=van_helsing_sample.model_dump())
    response = client.delete(f"/explorer/{van_helsing_sample.name}")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert (
        client.get(f"/explorer/{van_helsing_sample.name}").status_code
        == status.HTTP_404_NOT_FOUND
    )


def test_delete_missing():
    response = client.delete("/explorer/nonexistent")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "not found" in response.json()["detail"].lower()
    assert "explorer" in response.json()["detail"].lower()
    assert "nonexistent" in response.json()["detail"].lower()
