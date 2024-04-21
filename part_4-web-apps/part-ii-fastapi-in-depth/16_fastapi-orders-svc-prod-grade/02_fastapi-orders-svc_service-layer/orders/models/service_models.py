"""
Classes that represent the domain objects of the Orders service. These are the
objects that manage the data of the order and that are returned by the
OrdersRepository.
"""

from datetime import datetime
from uuid import UUID

import requests

from orders.models.data_models import OrderModel
from orders.models.shared_models import Size, Status
from orders.service.exceptions import APIIntegrationError, InvalidActionError


class OrderItem:
    """Represents each of the items in an Order"""

    def __init__(self, id_: UUID, product: str, quantity: int, size: Size):
        self.id = id_
        self.product = product
        self.quantity = quantity
        self.size = size

    def dict(self):
        return {
            "product": self.product,
            "size": self.size,
            "quantity": self.quantity,
        }


class Order:
    """Represents an Order"""

    def __init__(
        self,
        id_: UUID,
        created: datetime,
        items: list[OrderItem],
        status: Status,
        schedule_id: UUID | None = None,
        delivery_id: UUID | None = None,
        order_: OrderModel | None = None,
    ):
        self._order = order_
        self._id = id_
        self._created = created
        self.items = [OrderItem(**item) for item in items]  # type: ignore
        self._status = status
        self.schedule_id = schedule_id
        self.delivery_id = delivery_id

    @property
    def id(self) -> UUID | None:
        return self._id or (self._order.id if self._order else None) # type: ignore

    @property
    def created(self) -> datetime | None:
        return self._created or (self._order.created if self._order else None)  # type: ignore

    @property
    def status(self) -> Status:
        return self._status or (self._order.status if self._order else None)  # type: ignore

    def dict(self):
        return {
            "id": self.id,
            "order": [item.dict() for item in self.items],
            "status": self.status,
            "created": self.created,
        }

    def cancel(self):
        if self.status == "progress":
            response = requests.post(
                f"http://localhost:3000/kitchen/schedules/{self.schedule_id}/cancel",
                timeout=10,
            )
            if response.status_code == 200:
                return
            else:
                raise APIIntegrationError(
                    f"Could not cancel order with id {self.id}"
                )
        if self.status == "delivery":
            raise InvalidActionError(
                f"Cannot cancel order in delivery: {self.id}"
            )

    def pay(self):
        response = requests.post(
            "http://localhost:3001/payments",
            json={"order_id": self.id},
            timeout=10,
        )
        if response.status_code == 201:
            return
        else:
            raise APIIntegrationError(
                f"Could not process payment for order with id {self.id}"
            )

    def schedule(self):
        response = requests.post(
            "http://localhost:3000/kitchen/schedules",
            json={"order": [item.dict() for item in self.items]},
            timeout=10,
        )
        if response.status_code == 201:
            return response.json()["id"]
        else:
            raise APIIntegrationError(
                f"Could not schedule order with id {self.id}"
            )
