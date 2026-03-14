"""Schemas for the web application."""

from pydantic import BaseModel


class HelloMessageSchema(BaseModel):
    """Schema for returning a hello message."""

    text: str
