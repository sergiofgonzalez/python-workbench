"""Illustrates the basics of FastAPI header parameters."""

from typing import Annotated

from fastapi import FastAPI, Header
from pydantic import BaseModel

app = FastAPI()


@app.get("/items/")
async def read_items(
    user_agent: Annotated[str, Header()],
) -> dict[str, str]:
    """Path operation."""
    return {"User-Agent": user_agent}


@app.get("/v2/items/")
async def read_items_v2(
    x_token: Annotated[list[str] | None, Header()] = None,
) -> dict[str, list[str] | None]:
    """Path operation."""
    return {"X-Token": x_token}


class CommonHeaders(BaseModel):
    """Model for common headers."""

    host: str
    save_date: bool
    if_modified_since: str | None = None
    traceparent: str | None = None
    x_tag: list[str] | None = []


@app.get("/v3/items/")
async def read_items_v3(
    common_headers: Annotated[CommonHeaders, Header()],
) -> dict[str, str | bool | list[str] | None]:
    """Path operation."""
    return {**common_headers.model_dump()}


class CommonHeadersV2(BaseModel):
    """Model for common headers."""

    host: str
    save_date: bool
    if_modified_since: str | None = None
    traceparent: str | None = None
    x_tag: list[str] | None = []

    model_config = {"extra": "forbid"}


@app.get("/v4/items/")
async def read_items_v4(
    common_headers: Annotated[CommonHeadersV2, Header()],
) -> dict[str, str | bool | list[str] | None]:
    """Path operation."""
    return {**common_headers.model_dump()}


@app.get("/v5/items/")
async def read_items_v5(
    x_token: Annotated[str, Header(convert_underscores=False)],
) -> dict[str, str | bool | list[str] | None]:
    """Path operation."""
    return {"X_Token": x_token}
