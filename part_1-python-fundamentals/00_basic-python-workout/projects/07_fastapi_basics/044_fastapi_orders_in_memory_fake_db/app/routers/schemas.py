"""Schemas for the web application."""

from datetime import datetime
from enum import StrEnum
from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, Field


class SizeEnum(StrEnum):
    """Enumeration for product sizes."""

    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"


class StatusEnum(StrEnum):
    """Enumeration for order statuses."""

    CREATED = "created"
    PROGRESS = "progress"
    CANCELLED = "cancelled"
    DISPATCHED = "dispatched"
    DELIVERED = "delivered"


class OrderItemSchema(BaseModel):
    """Schema for an order item."""

    product: str
    size: SizeEnum
    quantity: Annotated[int, Field(ge=1)] = 1


class CreateOrderSchema(BaseModel):
    """Schema for creating an order."""

    items: Annotated[list[OrderItemSchema], Field(min_length=1)]


class GetOrderSchema(BaseModel):
    """Schema for retrieving an order."""

    id: UUID
    created: datetime
    status: StatusEnum
    items: list[OrderItemSchema]


class GetOrdersSchema(BaseModel):
    """Schema for retrieving multiple orders."""

    orders: list[GetOrderSchema]
