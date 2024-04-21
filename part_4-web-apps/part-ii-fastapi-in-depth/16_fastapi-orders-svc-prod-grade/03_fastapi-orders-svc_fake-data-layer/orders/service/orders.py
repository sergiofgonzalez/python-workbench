"""
Implements the unified interface that will be used from the API layer.
"""


from orders.service.exceptions import OrderNotFoundError
from orders.repository.orders_repository import OrdersRepository
from orders.models.service_models import Order


class OrdersService:
    """
    Encapsulates the capabilities of the orders domain and takes care of using
    the Orders repository to get orders objects and perform actions on them.
    """

    def __init__(self, orders_repository: OrdersRepository):
        self.orders_repository = orders_repository

    def place_order(self, items, user_id) -> Order:
        return self.orders_repository.add(items, user_id)

    def get_order(self, order_id, **filters) -> Order:
        order = self.orders_repository.get(order_id, **filters)
        if order is not None:
            return order
        else:
            raise OrderNotFoundError(f"Order with ID {order_id} not found")

    def update_order(self, order_id, user_id, **payload) -> Order:
        order = self.orders_repository.get(order_id, user_id=user_id)
        if order is not None:
            return self.orders_repository.update(order_id, **payload)
        else:
            raise OrderNotFoundError(
                f"Can't update order {order_id}: not found"
            )

    def list_orders(self, **filters) -> list[Order]:
        limit = filters.pop("limit", None)
        return self.orders_repository.list(limit, **filters)

    def pay_order(self, order_id, user_id) -> Order:
        order = self.orders_repository.get(order_id, user_id=user_id)
        if order is None:
            raise OrderNotFoundError(f"Can't pay order {order_id}: not found")
        order.pay()
        schedule_id = order.schedule()
        return self.orders_repository.update(
            order_id, status="progress", schedule_id=schedule_id
        )

    def cancel_order(self, order_id, user_id) -> Order:
        order = self.orders_repository.get(order_id, user_id=user_id)
        if order is None:
            raise OrderNotFoundError(
                f"Can't cancel order {order_id}: not found"
            )
        order.cancel()
        return self.orders_repository.update(order_id, status="cancelled")

    def delete_order(self, order_id, user_id) -> None:
        order = self.orders_repository.get(order_id, user_id=user_id)
        if order is None:
            raise OrderNotFoundError(
                f"Can't delete order {order_id}: not found"
            )
        return self.orders_repository.delete(order_id)
