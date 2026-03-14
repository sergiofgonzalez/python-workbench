"""Greeter router: contains all path operations related to greetings."""

from fastapi import APIRouter

from app.routers.schemas import (
    HelloMessageSchema,
)

router = APIRouter(prefix="/greetings", tags=["greetings"])


@router.get("/")
async def read_greetings() -> HelloMessageSchema:
    """Get a hello message."""
    return HelloMessageSchema(text="Hello, world!")
