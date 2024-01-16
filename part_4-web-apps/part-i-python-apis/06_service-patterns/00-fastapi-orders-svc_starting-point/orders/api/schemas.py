"""Pydantic schema specs: these are kept in sync with OpenAPI schema (manually)
"""
from datetime import datetime
from enum import Enum
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, conint, conlist, validator


class Size(Enum):
    SMALL = "small"
    MEDIUM = "medium"
    BIG = "big"


class Status(Enum):
    CREATED = "created"
    PROGRESS = "progress"
    CANCELLED = "cancelled"
    DISPATCHED = "dispatched"
    DELIVERED = "delivered"


class OrderItemSchema(BaseModel):
    model_config = ConfigDict(extra="forbid")

    product: str
    size: Size
    quantity: Optional[conint(ge=1, strict=True)] = 1

    @validator("quantity")
    @classmethod
    def quantity_not_null(cls, value):
        assert value is not None, "quantity must not be None"
        return value


class CreateOrderSchema(BaseModel):
    model_config = ConfigDict(extra="forbid")

    order: conlist(OrderItemSchema, min_length=1)


class GetOrderSchema(CreateOrderSchema):
    model_config = ConfigDict(extra="forbid")

    id: UUID
    created: datetime
    status: Status


class GetOrdersSchema(BaseModel):
    model_config = ConfigDict(extra="forbid")

    orders: List[GetOrderSchema]
