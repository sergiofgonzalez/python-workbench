"""Test the /greetings/* resource."""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_read_greetings() -> None:
    """Test the GET greetings endpoint."""
    response = client.get(
        "/greetings/",
    )
    assert response.status_code == 200
    assert response.json() == {"text": "Hello, world!"}
