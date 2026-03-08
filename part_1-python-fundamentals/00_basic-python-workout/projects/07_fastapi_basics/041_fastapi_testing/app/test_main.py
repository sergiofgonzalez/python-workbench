"""main.py tests without using a /test directory."""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_read_item() -> None:
    """Test the GET item endpoint."""
    response = client.get(
        "/items/foo",
        headers={"X-Token": "***"},
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": "foo",
        "title": "Foo",
        "description": "The Foo item",
    }


def test_read_item_invalid_token() -> None:
    """Test the GET item endpoint with an invalid token."""
    response = client.get(
        "/items/foo",
        headers={"X-Token": "invalid-token"},
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid X-Token header"}


def test_read_item_not_found() -> None:
    """Test the GET item endpoint with a non-existent item."""
    response = client.get(
        "/items/nonexistent",
        headers={"X-Token": "***"},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}


def test_create_item() -> None:
    """Test the POST item endpoint."""
    new_item = {
        "id": "baz",
        "title": "Baz",
        "description": "The Baz item",
    }
    response = client.post(
        "/items/",
        json=new_item,
        headers={"X-Token": "***"},
    )
    assert response.status_code == 200
    assert response.json() == new_item


def test_create_item_invalid_token() -> None:
    """Test the POST item endpoint with an invalid token."""
    new_item = {
        "id": "baz",
        "title": "Baz",
        "description": "The Baz item",
    }
    response = client.post(
        "/items/",
        json=new_item,
        headers={"X-Token": "invalid-token"},
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid X-Token header"}


def test_create_item_duplicate() -> None:
    """Test the POST item endpoint with an existing item ID."""
    existing_item = {
        "id": "foo",
        "title": "Foo",
        "description": "The Foo item",
    }
    response = client.post(
        "/items/",
        json=existing_item,
        headers={"X-Token": "***"},
    )
    assert response.status_code == 409
    assert response.json() == {"detail": "Item already exists"}
