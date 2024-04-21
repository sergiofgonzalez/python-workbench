"""Implements the Repository pattern for Orders"""

from orders.models.data_models import OrderItemModel, OrderModel
from orders.models.service_models import Order


class OrdersRepository:
    """Repository class for Orders"""

    def __init__(self, session) -> None:
        self.session = session

    def add(self, items, user_id) -> Order:
        record = OrderModel(
            items=[OrderItemModel(**item) for item in items], user_id=user_id
        )
        self.session.add(record)
        return Order(**record.dict(), order_=record)

    def _get(self, id_, **filters) -> OrderModel:
        return (
            self.session.query(OrderModel)
            .filter(OrderModel.id == str(id_))
            .filter_by(**filters)
            .first()
        )

    def get(self, id_, **filters) -> Order | None:
        order = self._get(id_, **filters)
        if order is not None:
            return Order(**order.dict())

    def list(self, limit=None, **filters) -> list[Order]:
        query = self.session.query(OrderModel)
        if "cancelled" in filters:
            cancelled = filters.pop("cancelled")
            if cancelled:
                query = query.filter(OrderModel.status == "cancelled")
            else:
                query = query.filter(OrderModel.status != "cancelled")
        records = query.filter_by(**filters).limit(limit).all()
        return [Order(**record.dict()) for record in records]

    def update(self, id_, **payload) -> Order:
        record = self._get(id_)
        if "items" in payload:
            for item in record.items:
                self.session.delete(item)
            record.items = [
                OrderItemModel(**item) for item in payload.pop("items")
            ]
        for key, value in payload.items():
            setattr(record, key, value)
        return Order(**record.dict())

    def delete(self, id_) -> None:
        self.session.delete(self._get(id_))
