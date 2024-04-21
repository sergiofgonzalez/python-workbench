"""
Order service schemas for the web layer.
"""

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator

from orders.models.shared_models import Size, Status


class OrderItemSchema(BaseModel):
    """
    Pydantic schema for an order item.

    Attributes:
    - product: str
    - size: Size
    - quantity: Optional[int] (default 1)

    The quantity is optional, but if present, it must be an int >= 1.
    """

    # forbid extra attributes during schema initialization
    model_config = ConfigDict(extra="forbid")

    product: str
    size: Size

    # quantity is optional, but if present, it must be an int >= 1
    quantity: Optional[int] = Field(default=1, strict=True, ge=1)

    # ensure quantity is not None
    @field_validator("quantity")
    @classmethod
    def quantity_not_null(cls, value) -> int:
        assert value is not None, "quantity must not be None"
        return value


class CreateOrderSchema(BaseModel):
    """
    Pydantic schema for creating an order.

    Attributes:
    - order: List[OrderItemSchema]
    """

    # forbid extra attributes during schema initialization
    model_config = ConfigDict(extra="forbid")

    # order is a list with at least one OrderItemSchema item
    order: list[OrderItemSchema] = Field(..., min_length=1)


class GetOrderSchema(CreateOrderSchema):
    """
    Pydantic schema for getting an order. Inherits from CreateOrderSchema.

    Attributes:
    - id: UUID
    - created: datetime
    - status: Status
    - order: List[OrderItemSchema]
    """

    # forbid extra attributes during schema initialization
    model_config = ConfigDict(extra="forbid")

    id: UUID
    created: datetime
    status: Status


class GetOrdersSchema(BaseModel):
    """
    Pydantic schema for getting a list of orders.

    Attributes:
    - orders: List[GetOrderSchema]
    """

    # forbid extra attributes during schema initialization
    model_config = ConfigDict(extra="forbid")

    orders: list[GetOrderSchema]
