from fastapi.testclient import TestClient

from orders.app import app

test_client = TestClient(app=app)


def test_create_order_fails():
    bad_payload = {"order": [{"product": "coffee"}]}
    response = test_client.post("/orders", json=bad_payload)
    assert response.status_code == 422


def test_create_order_succeeds():
    good_payload = {"order": [{"product": "coffee", "size": "big"}]}
    response = test_client.post("/orders", json=good_payload)
    assert response.status_code == 201
