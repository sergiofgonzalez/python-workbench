"""Object definitions for the data access layer"""

import uuid
from datetime import datetime, timezone


def generate_uuid():
    return str(uuid.uuid4())


class OrderModel:
    """Fake implementation of an Order in the fake data access layer"""

    def __init__(
        self,
        /,
        id=None,
        user_id=None,
        items=None,
        status=None,
        created=None,
        schedule_id=None,
        delivery_id=None,
    ) -> None:
        self.__tablename__ = "order"
        self.id = id or generate_uuid()
        self.user_id = user_id
        self.items = items
        self.status = status or "created"
        self.created = created or datetime.now(timezone.utc)
        self.schedule_id = schedule_id
        self.delivery_id = delivery_id

    def dict(self):
        return {
            "id_": self.id,
            "items": [item.dict() for item in self.items or []],
            "status": self.status,
            "created": self.created,
            "schedule_id": self.schedule_id,
            "delivery_id": self.delivery_id,
        }


class OrderItemModel:
    """
    Fake implementation of an Item belonging to an Order to the data access
    layer.
    """

    def __init__(
        self, id=None, order_id=None, product=None, size=None, quantity=None
    ) -> None:
        self.__tablename__ = "order_item"
        self.id = id or generate_uuid()
        self.order_id = order_id
        self.product = product
        self.size = size
        self.quantity = quantity

    def dict(self):
        return {
            "id_": self.id,
            "product": self.product,
            "size": self.size,
            "quantity": self.quantity,
        }
