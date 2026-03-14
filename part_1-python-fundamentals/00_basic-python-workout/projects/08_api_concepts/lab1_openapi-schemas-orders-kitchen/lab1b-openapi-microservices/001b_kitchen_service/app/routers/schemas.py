"""Schemas for the web application."""
from pyexpat import model

import datetime
from datetime import datetime
from enum import StrEnum
from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, Field


class SizeEnum(StrEnum):
    """Enum for order item size."""

    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"


class ScheduledOrderItemSchema(BaseModel):
    """Schema for an item in an order."""
    model_config = {"extra": "forbid"}

    product: str
    size: SizeEnum
    quantity: Annotated[int, Field(ge=1)] = 1


class ScheduledOrderStatusSchema(StrEnum):
    """Enum for the status of a scheduled order."""

    PENDING = "pending"
    PROGRESS = "progress"
    CANCELLED = "cancelled"
    FINISHED = "finished"


class ScheduledOrderSchema(BaseModel):
    """Schema for an order scheduled for production."""
    model_config = {"extra": "forbid"}

    order: Annotated[list[ScheduledOrderItemSchema], Field(min_length=1)]


class GetScheduledOrderSchema(BaseModel):
    """Schema for retrieving an order scheduled for production."""

    schedule_id: UUID
    scheduled: datetime
    status: ScheduledOrderStatusSchema
    order: Annotated[list[ScheduledOrderItemSchema], Field(min_length=1)]


class GetScheduledOrdersSchema(BaseModel):
    """Schema for retrieving a list of orders scheduled for production."""

    schedules: list[GetScheduledOrderSchema]


class QueryScheduledOrdersSchema(BaseModel):
    """Schema for querying orders scheduled for production."""
    model_config = {"extra": "forbid"}

    progress: bool | None = None
    limit: Annotated[int | None, Field(ge=1)] = None
    since: datetime | None = None
