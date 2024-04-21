"""
Shared domain objects used across multiple layers.
"""

from enum import Enum


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
