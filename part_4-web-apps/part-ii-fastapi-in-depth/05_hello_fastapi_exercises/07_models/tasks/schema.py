"""Task app schemas describing the domain model of the app"""
from datetime import datetime
from typing import Annotated

from pydantic import UUID4, BaseModel, Field, StringConstraints


class TaskIn(BaseModel):
    title: Annotated[str, StringConstraints(min_length=2, max_length=63)]
    description: Annotated[
        str | None, StringConstraints(min_length=2, max_length=255)
    ] = None
    urgency: Annotated[int, Field(ge=1, le=9)]


class Task(BaseModel):
    id: UUID4
    title: Annotated[str, StringConstraints(min_length=2, max_length=63)]
    description: Annotated[
        str | None, StringConstraints(min_length=2, max_length=255)
    ] = None
    urgency: Annotated[int, Field(ge=1, le=9)]
    creation_ts: datetime


class TaskOut(BaseModel):
    title: Annotated[str, StringConstraints(min_length=2, max_length=63)]
    description: Annotated[
        str | None, StringConstraints(min_length=2, max_length=255)
    ] = None
    urgency: Annotated[int, Field(ge=1, le=9)]
    creation_ts: datetime
