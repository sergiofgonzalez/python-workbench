"""Unit tests for the orders API endpoints."""

import yaml
from fastapi import status
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

VALID_ORDER_PAYLOAD: dict[str, list[dict[str, str | int]]] = {
    "order": [{"product": "Margherita", "size": "small", "quantity": 2}],
}


def _create_order() -> str:
    """Create a single order and return its order_id."""
    response = client.post("/orders/", json=VALID_ORDER_PAYLOAD)
    return response.json()["order_id"]


def test_create_order() -> None:
    """POST /orders/ with a valid payload returns 201 and the created order."""
    # Act
    response = client.post("/orders/", json=VALID_ORDER_PAYLOAD)

    # Assert
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert "order_id" in data
    assert "created" in data
    assert data["status"] == "created"
    assert data["order"] == VALID_ORDER_PAYLOAD["order"]


def test_create_order_default_quantity() -> None:
    """POST /orders/ without quantity defaults to 1."""
    # Arrange
    payload = {"order": [{"product": "Pepperoni", "size": "medium"}]}

    # Act
    response = client.post("/orders/", json=payload)

    # Assert
    assert response.status_code == status.HTTP_201_CREATED
    item = response.json()["order"][0]
    assert item["quantity"] == 1


def test_create_order_multiple_items() -> None:
    """POST /orders/ with multiple items returns all items."""
    # Arrange
    payload = {
        "order": [
            {"product": "Margherita", "size": "small", "quantity": 1},
            {"product": "Calzone", "size": "large", "quantity": 3},
        ],
    }

    # Act
    response = client.post("/orders/", json=payload)

    # Assert
    assert response.status_code == status.HTTP_201_CREATED
    assert len(response.json()["order"]) == 2


def test_create_order_empty_order_list_returns_422() -> None:
    """POST /orders/ with an empty order list returns 422."""
    # Arrange
    payload = {"order": []}

    # Act
    response = client.post("/orders/", json=payload)

    # Assert
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


def test_create_order_missing_product_returns_422() -> None:
    """POST /orders/ with item missing product returns 422."""
    # Arrange
    payload = {"order": [{"size": "small", "quantity": 1}]}

    # Act
    response = client.post("/orders/", json=payload)

    # Assert
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


def test_create_order_missing_size_returns_422() -> None:
    """POST /orders/ with item missing size returns 422."""
    # Arrange
    payload = {"order": [{"product": "Hawaiian", "quantity": 1}]}

    # Act
    response = client.post("/orders/", json=payload)

    # Assert
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


def test_create_order_invalid_size_returns_422() -> None:
    """POST /orders/ with invalid size enum value returns 422."""
    # Arrange
    payload = {"order": [{"product": "Quattro Formaggi", "size": "gigantic"}]}

    # Act
    response = client.post("/orders/", json=payload)

    # Assert
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


def test_create_order_quantity_zero_returns_422() -> None:
    """POST /orders/ with quantity zero returns 422."""
    # Arrange
    payload = {"order": [{"product": "Diavola", "size": "medium", "quantity": 0}]}

    # Act
    response = client.post("/orders/", json=payload)

    # Assert
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


def test_create_order_extra_field_on_body_returns_422() -> None:
    """POST /orders/ with extra field on body returns 422."""
    # Arrange
    payload = {
        "order": [{"product": "Margherita", "size": "small"}],
        "discount": "10%",
    }

    # Act
    response = client.post("/orders/", json=payload)

    # Assert
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


def test_create_order_extra_field_on_item_returns_422() -> None:
    """POST /orders/ with extra field on order item returns 422."""
    # Arrange
    payload = {
        "order": [
            {"product": "Capricciosa", "size": "large", "topping": "extra cheese"},
        ],
    }

    # Act
    response = client.post("/orders/", json=payload)

    # Assert
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


def test_create_order_missing_order_field_returns_422() -> None:
    """POST /orders/ with empty body returns 422."""
    # Act
    response = client.post("/orders/", json={})

    # Assert
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


# --- GET /orders/ ---


def test_read_orders_empty() -> None:
    """GET /orders/ with no data returns an empty list."""
    # Act
    response = client.get("/orders/")

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"orders": []}


def test_read_orders_returns_all() -> None:
    """GET /orders/ returns all created orders."""
    # Arrange
    _create_order()
    _create_order()

    # Act
    response = client.get("/orders/")

    # Assert
    assert response.status_code == status.HTTP_200_OK
    orders = response.json()["orders"]
    assert len(orders) == 2
    for order in orders:
        assert "order_id" in order
        assert "created" in order
        assert "status" in order
        assert "order" in order


def test_read_orders_filter_cancelled_true() -> None:
    """GET /orders/?cancelled=true returns only cancelled orders."""
    # Arrange
    cancelled_id = _create_order()
    _create_order()
    client.post(f"/orders/{cancelled_id}/cancel")

    # Act
    response = client.get("/orders/", params={"cancelled": True})

    # Assert
    assert response.status_code == status.HTTP_200_OK
    orders = response.json()["orders"]
    assert len(orders) == 1
    assert orders[0]["order_id"] == cancelled_id


def test_read_orders_filter_cancelled_false() -> None:
    """GET /orders/?cancelled=false returns only non-cancelled orders."""
    # Arrange
    cancelled_id = _create_order()
    active_id = _create_order()
    client.post(f"/orders/{cancelled_id}/cancel")

    # Act
    response = client.get("/orders/", params={"cancelled": False})

    # Assert
    assert response.status_code == status.HTTP_200_OK
    orders = response.json()["orders"]
    assert len(orders) == 1
    assert orders[0]["order_id"] == active_id


def test_read_orders_filter_cancelled_not_set() -> None:
    """GET /orders/ without cancelled param returns all orders."""
    # Arrange
    cancelled_id = _create_order()
    _create_order()
    client.post(f"/orders/{cancelled_id}/cancel")

    # Act
    response = client.get("/orders/")

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()["orders"]) == 2


def test_read_orders_limit_and_cancelled() -> None:
    """GET /orders/?cancelled=true&limit=1 applies both filters."""
    # Arrange
    id_1 = _create_order()
    id_2 = _create_order()
    _create_order()
    client.post(f"/orders/{id_1}/cancel")
    client.post(f"/orders/{id_2}/cancel")

    # Act
    response = client.get(
        "/orders/",
        params={"cancelled": True, "limit": 1},
    )

    # Assert
    assert response.status_code == status.HTTP_200_OK
    orders = response.json()["orders"]
    assert len(orders) == 1
    assert orders[0]["status"] == "cancelled"


def test_read_orders_limit() -> None:
    """GET /orders/?limit=2 returns at most 2 orders."""
    # Arrange
    _create_order()
    _create_order()
    _create_order()

    # Act
    response = client.get("/orders/", params={"limit": 2})

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()["orders"]) == 2


def test_read_orders_limit_zero_returns_422() -> None:
    """GET /orders/?limit=0 returns 422 because limit must be >= 1."""
    # Act
    response = client.get("/orders/", params={"limit": 0})

    # Assert
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


def test_read_orders_limit_negative_returns_422() -> None:
    """GET /orders/?limit=-1 returns 422 because limit must be >= 1."""
    # Act
    response = client.get("/orders/", params={"limit": -1})

    # Assert
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


# --- GET /orders/{order_id} ---


def test_read_order() -> None:
    """GET /orders/{order_id} returns the order."""
    # Arrange
    order_id = _create_order()

    # Act
    response = client.get(f"/orders/{order_id}")

    # Assert
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["order_id"] == order_id
    assert data["status"] == "created"
    assert data["order"] == VALID_ORDER_PAYLOAD["order"]


def test_read_order_not_found() -> None:
    """GET /orders/{order_id} with nonexistent UUID returns 404."""
    # Act
    response = client.get(
        "/orders/00000000-0000-0000-0000-000000000000",
    )

    # Assert
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Order not found"


def test_read_order_invalid_uuid_returns_422() -> None:
    """GET /orders/{order_id} with invalid UUID returns 422."""
    # Act
    response = client.get("/orders/not-a-uuid")

    # Assert
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


# --- PUT /orders/{order_id} ---


def test_update_order() -> None:
    """PUT /orders/{order_id} replaces items, preserves status and created."""
    # Arrange
    order_id = _create_order()
    original = client.get(f"/orders/{order_id}").json()
    new_payload = {
        "order": [{"product": "Quattro Stagioni", "size": "large", "quantity": 1}],
    }

    # Act
    response = client.put(f"/orders/{order_id}", json=new_payload)

    # Assert
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["order"] == new_payload["order"]
    assert data["status"] == original["status"]
    assert data["created"] == original["created"]


def test_update_order_preserves_status() -> None:
    """PUT /orders/{order_id} after pay preserves the in-progress status."""
    # Arrange
    order_id = _create_order()
    client.post(f"/orders/{order_id}/pay")
    new_payload = {
        "order": [{"product": "Tonno e Cipolla", "size": "medium"}],
    }

    # Act
    response = client.put(f"/orders/{order_id}", json=new_payload)

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["status"] == "progress"


def test_update_order_not_found() -> None:
    """PUT /orders/{order_id} with nonexistent UUID returns 404."""
    # Arrange
    payload = {
        "order": [{"product": "Margherita", "size": "small"}],
    }

    # Act
    response = client.put(
        "/orders/00000000-0000-0000-0000-000000000000",
        json=payload,
    )

    # Assert
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Order not found"


def test_update_order_empty_order_list_returns_422() -> None:
    """PUT /orders/{order_id} with empty order list returns 422."""
    # Arrange
    order_id = _create_order()

    # Act
    response = client.put(f"/orders/{order_id}", json={"order": []})

    # Assert
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


# --- DELETE /orders/{order_id} ---


def test_delete_order() -> None:
    """DELETE /orders/{order_id} removes the order."""
    # Arrange
    order_id = _create_order()

    # Act
    response = client.delete(f"/orders/{order_id}")

    # Assert
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert client.get(f"/orders/{order_id}").status_code == status.HTTP_404_NOT_FOUND


def test_delete_order_not_found() -> None:
    """DELETE /orders/{order_id} with nonexistent UUID returns 404."""
    # Act
    response = client.delete(
        "/orders/00000000-0000-0000-0000-000000000000",
    )

    # Assert
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Order not found"


# --- POST /orders/{order_id}/cancel ---


def test_cancel_order() -> None:
    """POST /orders/{order_id}/cancel sets status to cancelled."""
    # Arrange
    order_id = _create_order()

    # Act
    response = client.post(f"/orders/{order_id}/cancel")

    # Assert
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["status"] == "cancelled"
    assert data["order_id"] == order_id


def test_cancel_order_not_found() -> None:
    """POST /orders/{order_id}/cancel with nonexistent UUID returns 404."""
    # Act
    response = client.post(
        "/orders/00000000-0000-0000-0000-000000000000/cancel",
    )

    # Assert
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Order not found"


# --- POST /orders/{order_id}/pay ---


def test_pay_order() -> None:
    """POST /orders/{order_id}/pay sets status to progress."""
    # Arrange
    order_id = _create_order()

    # Act
    response = client.post(f"/orders/{order_id}/pay")

    # Assert
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["status"] == "progress"
    assert data["order_id"] == order_id


def test_pay_order_not_found() -> None:
    """POST /orders/{order_id}/pay with nonexistent UUID returns 404."""
    # Act
    response = client.post(
        "/orders/00000000-0000-0000-0000-000000000000/pay",
    )

    # Assert
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Order not found"


# --- GET /openapi.yaml ---


def test_openapi_yaml_returns_200() -> None:
    """GET /openapi.yaml returns 200 with application/yaml content type."""
    # Act
    response = client.get("/openapi.yaml")

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert response.headers["content-type"] == "application/yaml"


def test_openapi_yaml_is_valid_yaml() -> None:
    """GET /openapi.yaml returns valid YAML with expected OpenAPI keys."""
    # Act
    response = client.get("/openapi.yaml")
    schema = yaml.safe_load(response.text)

    # Assert
    assert "openapi" in schema
    assert "info" in schema
    assert "paths" in schema
