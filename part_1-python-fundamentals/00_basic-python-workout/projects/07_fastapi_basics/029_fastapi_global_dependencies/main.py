"""Illustrates how to set up dependencies for all the path operations."""

from typing import Annotated

from fastapi import Depends, FastAPI, Header, HTTPException


async def x_token_header_validator(
    x_token: Annotated[str | None, Header()] = None,
) -> None:
    """A dependency that validates the presence of an X-Token header."""
    if x_token != "fake-secret-token":  # noqa: S105
        raise HTTPException(status_code=400, detail="X-Token is invalid or missing")


async def x_key_header_validator(
    x_key: Annotated[str | None, Header()] = None,
) -> str:
    """A dependency that validates the presence of an X-Key header."""
    if x_key != "fake-secret-key":
        raise HTTPException(status_code=400, detail="X-Key is invalid or missing")
    return x_key


app = FastAPI(
    dependencies=[Depends(x_token_header_validator), Depends(x_key_header_validator)],
)


@app.get("/items/")
async def read_items() -> list[dict[str, str]]:
    """Path operation for the GET /items/ endpoint."""
    return [{"item": "Foo"}, {"item": "Bar"}]


@app.get("/users/")
async def read_users() -> list[dict[str, str]]:
    """Path operation for the GET /users/ endpoint."""
    return [{"user": "Alice"}, {"user": "Bob"}]
