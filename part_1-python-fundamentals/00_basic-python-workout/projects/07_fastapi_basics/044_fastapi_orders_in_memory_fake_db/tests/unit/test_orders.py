"""main.py tests without using a /tests directory."""

from collections.abc import Iterable

import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_teardown() -> Iterable[None]:
    """Delete all orders after each test automatically."""
    # Setup code can be added here if needed, but not needed for these tests
    yield
    orders_to_clear = client.get("/orders/").json()["orders"]
    for order in orders_to_clear:
        client.delete(f"/orders/{order['id']}")


def test_read_orders_empty() -> None:
    """Test the GET order endpoint when no orders exist."""
    response = client.get(
        "/orders/",
    )
    assert response.status_code == 200
    assert response.json() == {"orders": []}


def test_read_orders_single_order_single_item() -> None:
    """Test the GET order endpoint when one order exists."""
    # Create a new order
    new_order = {
        "items": [
            {"product": "Item 1", "size": "small", "quantity": 2},
        ],
    }
    create_response = client.post(
        "/orders/",
        json=new_order,
    )
    assert create_response.status_code == 201
    created_order = create_response.json()

    # Get all orders
    response = client.get(
        "/orders/",
    )
    assert response.status_code == 200
    assert response.json() == {"orders": [created_order]}


def test_read_orders_single_order_several_items() -> None:
    """Test the GET order endpoint when one order exists."""
    # Create a new order
    new_order = {
        "items": [
            {"product": "Item 1", "size": "small", "quantity": 2},
            {"product": "Item 2", "size": "medium", "quantity": 3},
            {"product": "Item 3", "size": "large"},
        ],
    }
    create_response = client.post(
        "/orders/",
        json=new_order,
    )
    assert create_response.status_code == 201
    created_order = create_response.json()

    # Get all orders
    response = client.get(
        "/orders/",
    )
    assert response.status_code == 200
    assert response.json() == {"orders": [created_order]}


def test_read_orders_multiple_orders_several_items() -> None:
    """Test the GET order endpoint when multiple orders exist."""
    # Create a new order
    new_order_1 = {
        "items": [
            {"product": "Item 1", "size": "small", "quantity": 2},
            {"product": "Item 2", "size": "medium", "quantity": 3},
            {"product": "Item 3", "size": "large"},
        ],
    }
    create_response = client.post(
        "/orders/",
        json=new_order_1,
    )
    assert create_response.status_code == 201
    created_order_1 = create_response.json()

    # Create another order
    new_order_2 = {
        "items": [
            {"product": "Item 4", "size": "small", "quantity": 4},
            {"product": "Item 5", "size": "medium", "quantity": 5},
            {"product": "Item 6", "size": "large", "quantity": 6},
        ],
    }
    create_response = client.post(
        "/orders/",
        json=new_order_2,
    )
    assert create_response.status_code == 201
    created_order_2 = create_response.json()

    # Get all orders
    response = client.get(
        "/orders/",
    )
    assert response.status_code == 200
    assert response.json() == {"orders": [created_order_1, created_order_2]}


def test_create_order() -> None:
    """Test the POST order endpoint."""
    new_order = {
        "items": [
            {"product": "Item 1", "size": "small", "quantity": 2},
            {"product": "Item 2", "size": "medium", "quantity": 3},
            {"product": "Item 3", "size": "large"},
        ],
    }
    response = client.post(
        "/orders/",
        json=new_order,
    )
    assert response.status_code == 201
    new_order["items"][2].update(
        {"quantity": 1},
    )  # Default quantity should be 1 for Item 3
    created_order = response.json()
    assert created_order["id"] is not None
    assert created_order["created"] is not None
    assert created_order["status"] == "created"
    assert created_order["items"] == new_order["items"]


def test_create_order_invalid_size() -> None:
    """Test the POST order endpoint with an invalid size."""
    new_order = {
        "items": [
            {"product": "Item 1", "size": "invalid-size", "quantity": 2},
        ],
    }
    response = client.post(
        "/orders/",
        json=new_order,
    )
    assert response.status_code == 422


def test_create_order_invalid_quantity() -> None:
    """Test the POST order endpoint with an invalid quantity."""
    new_order = {
        "items": [
            {"product": "Item 1", "size": "small", "quantity": 0},
        ],
    }
    response = client.post(
        "/orders/",
        json=new_order,
    )
    assert response.status_code == 422


def test_create_order_missing_product() -> None:
    """Test the POST order endpoint with a missing product."""
    new_order = {
        "items": [
            {"size": "small", "quantity": 2},
        ],
    }
    response = client.post(
        "/orders/",
        json=new_order,
    )
    assert response.status_code == 422


def test_create_order_missing_size() -> None:
    """Test the POST order endpoint with a missing size."""
    new_order = {
        "items": [
            {"product": "Item 1", "quantity": 2},
        ],
    }
    response = client.post(
        "/orders/",
        json=new_order,
    )
    assert response.status_code == 422


def test_create_order_missing_quantity() -> None:
    """Test the POST order endpoint with a missing quantity."""
    new_order = {
        "items": [
            {"product": "Item 1", "size": "small"},
        ],
    }
    response = client.post(
        "/orders/",
        json=new_order,
    )
    assert response.status_code == 201
    created_order = response.json()
    assert created_order["items"][0]["quantity"] == 1  # Default quantity should be 1


def test_create_order_empty_items() -> None:
    """Test the POST order endpoint with an empty items list."""
    new_order = {
        "items": [],
    }
    response = client.post(
        "/orders/",
        json=new_order,
    )
    assert response.status_code == 422


def test_create_order_missing_items() -> None:
    """Test the POST order endpoint with missing items."""
    new_order = {}
    response = client.post(
        "/orders/",
        json=new_order,
    )
    assert response.status_code == 422


def test_create_order_invalid_items_type() -> None:
    """Test the POST order endpoint with an invalid items type."""
    new_order = {
        "items": "invalid-type",
    }
    response = client.post(
        "/orders/",
        json=new_order,
    )
    assert response.status_code == 422


def test_create_order_invalid_item_structure() -> None:
    """Test the POST order endpoint with an invalid item structure."""
    new_order = {
        "items": [
            {"invalid_field": "value"},
        ],
    }
    response = client.post(
        "/orders/",
        json=new_order,
    )
    assert response.status_code == 422


def test_create_order_invalid_item_size() -> None:
    """Test the POST order endpoint with an invalid item size."""
    new_order = {
        "items": [
            {"product": "Item 1", "size": "invalid-size", "quantity": 2},
        ],
    }
    response = client.post(
        "/orders/",
        json=new_order,
    )
    assert response.status_code == 422


def test_read_order() -> None:
    """Test the GET order endpoint with a valid order ID."""
    # Create a new order
    new_order = {
        "items": [
            {"product": "Item 1", "size": "small", "quantity": 2},
        ],
    }
    create_response = client.post(
        "/orders/",
        json=new_order,
    )
    assert create_response.status_code == 201
    created_order = create_response.json()

    # Get the order by ID
    response = client.get(
        f"/orders/{created_order['id']}",
    )
    assert response.status_code == 200
    assert response.json() == created_order


def test_read_order_not_found() -> None:
    """Test the GET order endpoint with a non-existent order ID."""
    response = client.get(
        "/orders/00000000-0000-0000-0000-000000000000",
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Order not found"}


def test_read_order_invalid_id() -> None:
    """Test the GET order endpoint with an invalid order ID."""
    response = client.get(
        "/orders/invalid-id",
    )
    assert response.status_code == 422


def test_update_order() -> None:
    """Test the PUT order endpoint with a valid order ID."""
    # Create a new order
    new_order = {
        "items": [
            {"product": "Item 1", "size": "small", "quantity": 2},
        ],
    }
    create_response = client.post(
        "/orders/",
        json=new_order,
    )
    assert create_response.status_code == 201
    created_order = create_response.json()

    # Update the order
    updated_order_data = {
        "items": [
            {"product": "Item 1", "size": "small", "quantity": 3},
            {"product": "Item 2", "size": "medium", "quantity": 1},
        ],
    }
    update_response = client.put(
        f"/orders/{created_order['id']}",
        json=updated_order_data,
    )
    assert update_response.status_code == 200
    updated_order = update_response.json()
    assert updated_order["id"] == created_order["id"]
    assert updated_order["created"] == created_order["created"]
    assert updated_order["status"] == created_order["status"]
    assert updated_order["items"] == updated_order_data["items"]


def test_update_order_not_found() -> None:
    """Test the PUT order endpoint with a non-existent order ID."""
    updated_order_data = {
        "items": [
            {"product": "Item 1", "size": "small", "quantity": 3},
            {"product": "Item 2", "size": "medium", "quantity": 1},
        ],
    }
    response = client.put(
        "/orders/00000000-0000-0000-0000-000000000000",
        json=updated_order_data,
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Order not found"}


def test_update_order_invalid_id() -> None:
    """Test the PUT order endpoint with an invalid order ID."""
    updated_order_data = {
        "items": [
            {"product": "Item 1", "size": "small", "quantity": 3},
            {"product": "Item 2", "size": "medium", "quantity": 1},
        ],
    }
    response = client.put(
        "/orders/invalid-id",
        json=updated_order_data,
    )
    assert response.status_code == 422


def test_delete_order() -> None:
    """Test the DELETE order endpoint with a valid order ID."""
    # Create a new order
    new_order = {
        "items": [
            {"product": "Item 1", "size": "small", "quantity": 2},
        ],
    }
    create_response = client.post(
        "/orders/",
        json=new_order,
    )
    assert create_response.status_code == 201
    created_order = create_response.json()

    # Delete the order
    delete_response = client.delete(
        f"/orders/{created_order['id']}",
    )
    assert delete_response.status_code == 204

    # Verify the order is deleted
    get_response = client.get(
        f"/orders/{created_order['id']}",
    )
    assert get_response.status_code == 404
    assert get_response.json() == {"detail": "Order not found"}


def test_delete_order_not_found() -> None:
    """Test the DELETE order endpoint with a non-existent order ID."""
    response = client.delete(
        "/orders/00000000-0000-0000-0000-000000000000",
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Order not found"}


def test_delete_order_invalid_id() -> None:
    """Test the DELETE order endpoint with an invalid order ID."""
    response = client.delete(
        "/orders/invalid-id",
    )
    assert response.status_code == 422


def test_cancel_order_created() -> None:
    """Test the POST cancel order endpoint with a valid order ID."""
    # Create a new order
    new_order = {
        "items": [
            {"product": "Item 1", "size": "small", "quantity": 2},
        ],
    }
    create_response = client.post(
        "/orders/",
        json=new_order,
    )
    assert create_response.status_code == 201
    created_order = create_response.json()

    # Cancel the order
    cancel_response = client.post(
        f"/orders/{created_order['id']}/cancel",
    )
    assert cancel_response.status_code == 200
    cancelled_order = cancel_response.json()
    assert cancelled_order["id"] == created_order["id"]
    assert cancelled_order["created"] == created_order["created"]
    assert cancelled_order["status"] == "cancelled"
    assert cancelled_order["items"] == created_order["items"]


def test_cancel_order_progress() -> None:
    """Test the POST cancel order endpoint with a valid order ID."""
    # Create a new order
    new_order = {
        "items": [
            {"product": "Item 1", "size": "small", "quantity": 2},
        ],
    }
    create_response = client.post(
        "/orders/",
        json=new_order,
    )
    assert create_response.status_code == 201
    created_order = create_response.json()
    created_order["status"] = "progress"  # Manually set status to progress for testing

    # Pay the order to update its status to progress
    update_response = client.post(
        f"/orders/{created_order['id']}/pay",
        json={"items": created_order["items"]},
    )
    assert update_response.status_code == 200
    assert update_response.json()["status"] == "progress"

    # Cancel the order
    cancel_response = client.post(
        f"/orders/{created_order['id']}/cancel",
    )
    assert cancel_response.status_code == 200
    cancelled_order = cancel_response.json()
    assert cancelled_order["id"] == created_order["id"]
    assert cancelled_order["created"] == created_order["created"]
    assert cancelled_order["status"] == "cancelled"
    assert cancelled_order["items"] == created_order["items"]


def test_cancel_order_not_found() -> None:
    """Test the POST cancel order endpoint with a non-existent order ID."""
    response = client.post(
        "/orders/00000000-0000-0000-0000-000000000000/cancel",
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Order not found"}


def test_cancel_order_invalid_id() -> None:
    """Test the POST cancel order endpoint with an invalid order ID."""
    response = client.post(
        "/orders/invalid-id/cancel",
    )
    assert response.status_code == 422


def test_cancel_order_already_cancelled() -> None:
    """Test the POST cancel order endpoint with an already cancelled order."""
    # Create a new order
    new_order = {
        "items": [
            {"product": "Item 1", "size": "small", "quantity": 2},
        ],
    }
    create_response = client.post(
        "/orders/",
        json=new_order,
    )
    assert create_response.status_code == 201
    created_order = create_response.json()

    # Cancel the order
    cancel_response = client.post(
        f"/orders/{created_order['id']}/cancel",
    )
    assert cancel_response.status_code == 200

    # Cancel the order again
    cancel_response_again = client.post(
        f"/orders/{created_order['id']}/cancel",
    )
    assert cancel_response_again.status_code == 400


def test_pay_order() -> None:
    """Test the POST pay order endpoint with a valid order ID."""
    # Create a new order
    new_order = {
        "items": [
            {"product": "Item 1", "size": "small", "quantity": 2},
        ],
    }
    create_response = client.post(
        "/orders/",
        json=new_order,
    )
    assert create_response.status_code == 201
    created_order = create_response.json()

    # Pay the order
    pay_response = client.post(
        f"/orders/{created_order['id']}/pay",
    )
    assert pay_response.status_code == 200
    paid_order = pay_response.json()
    assert paid_order["id"] == created_order["id"]
    assert paid_order["created"] == created_order["created"]
    assert paid_order["status"] == "progress"
    assert paid_order["items"] == created_order["items"]


def test_pay_order_not_found() -> None:
    """Test the POST pay order endpoint with a non-existent order ID."""
    response = client.post(
        "/orders/00000000-0000-0000-0000-000000000000/pay",
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Order not found"}


def test_pay_order_invalid_id() -> None:
    """Test the POST pay order endpoint with an invalid order ID."""
    response = client.post(
        "/orders/invalid-id/pay",
    )
    assert response.status_code == 422


def test_pay_order_already_paid() -> None:
    """Test the POST pay order endpoint with an order that cannot be paid for."""
    # Create a new order
    new_order = {
        "items": [
            {"product": "Item 1", "size": "small", "quantity": 2},
        ],
    }
    create_response = client.post(
        "/orders/",
        json=new_order,
    )
    assert create_response.status_code == 201
    created_order = create_response.json()

    # Pay the order
    pay_response = client.post(
        f"/orders/{created_order['id']}/pay",
    )
    assert pay_response.status_code == 200

    # Pay the order again
    pay_response_again = client.post(
        f"/orders/{created_order['id']}/pay",
    )
    assert pay_response_again.status_code == 400


def test_pay_order_cancelled() -> None:
    """Test the POST pay order endpoint with a cancelled order."""
    # Create a new order
    new_order = {
        "items": [
            {"product": "Item 1", "size": "small", "quantity": 2},
        ],
    }
    create_response = client.post(
        "/orders/",
        json=new_order,
    )
    assert create_response.status_code == 201
    created_order = create_response.json()

    # Cancel the order
    cancel_response = client.post(
        f"/orders/{created_order['id']}/cancel",
    )
    assert cancel_response.status_code == 200

    # Pay the cancelled order
    pay_response = client.post(
        f"/orders/{created_order['id']}/pay",
    )
    assert pay_response.status_code == 400
