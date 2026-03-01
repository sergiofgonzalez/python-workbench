"""Common dependencies module."""

from typing import Annotated

from fastapi import Header, HTTPException


async def get_token_from_header(x_token: Annotated[str | None, Header()] = None) -> str:
    """Dependency function to get a token from the header."""
    if x_token is None:
        raise HTTPException(status_code=400, detail="X-Token header missing")
    return x_token


async def get_token_from_query(token: str | None = None) -> str:
    """Dependency function to get a token from the query parameters."""
    if token is None:
        raise HTTPException(status_code=400, detail="Token query parameter missing")
    return token
