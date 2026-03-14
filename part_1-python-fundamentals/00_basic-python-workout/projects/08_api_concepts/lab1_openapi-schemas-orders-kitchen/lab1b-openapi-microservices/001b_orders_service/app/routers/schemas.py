"""Schemas for the web application."""

from datetime import datetime
from enum import StrEnum
from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, Field


class StatusEnum(StrEnum):
    """Enum for order status."""

    CREATED = "created"
    IN_PROGRESS = "progress"
    CANCELLED = "cancelled"
    DISPATCHED = "dispatched"
    DELIVERED = "delivered"


class SizeEnum(StrEnum):
    """Enum for order item size."""

    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"


class OrderItemSchema(BaseModel):
    """Schema for an order item."""

    model_config = {"extra": "forbid"}

    product: str
    size: SizeEnum
    quantity: Annotated[int, Field(ge=1)] = 1


class CreateOrderSchema(BaseModel):
    """Schema for creating an order."""

    model_config = {"extra": "forbid"}

    order: Annotated[list[OrderItemSchema], Field(min_items=1)]


class GetOrderSchema(BaseModel):
    """Schema for a single order."""

    order_id: UUID
    created: datetime
    status: StatusEnum
    order: Annotated[list[OrderItemSchema], Field(min_items=1)]


class GetOrdersSchema(BaseModel):
    """Schema for a list of orders."""

    orders: list[GetOrderSchema]


class ReadOrdersQueryParams(BaseModel):
    """Schema for query parameters for reading orders."""

    model_config = {"extra": "forbid"}

    cancelled: bool | None = None
    limit: Annotated[int | None, Field(ge=1)] = None
