"""Object definitions for the data access layer"""
import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


def generate_uuid():
    return str(uuid.uuid4())


class OrderModel(Base):
    """Represents an Order in the data access layer"""

    __tablename__ = "order"

    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, nullable=False)
    items = relationship("OrderItemModel", backref="order")
    status = Column(String, nullable=False, default="created")
    created = Column(DateTime, default=datetime.utcnow())
    schedule_id = Column(String)
    delivery_id = Column(String)

    def dict(self):
        return {
            "id": self.id,
            "items": [item.dict() for item in self.items],
            "status": self.status,
            "created": self.created,
            "schedule_id": self.schedule_id,
            "delivery_id": self.delivery_id,
        }


class OrderItemModel(Base):
    """Represents an Item belonging to an Order to the data access layer"""
    __tablename__ = "order_item"

    id = Column(String, primary_key=True, default=generate_uuid)
    order_id = Column(
        Integer, ForeignKey("order.id")
    )  # NOTE: shouldn't this be string??
    product = Column(String, nullable=False)
    size = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)

    def dict(self):
        return {
            "id": self.id,
            "product": self.product,
            "size": self.size,
            "quantity": self.quantity,
        }
