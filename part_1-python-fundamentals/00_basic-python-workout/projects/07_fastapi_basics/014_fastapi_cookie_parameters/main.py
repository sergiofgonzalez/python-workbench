"""Illustrates the basics of FastAPI cookie parameters."""

from typing import Annotated

from fastapi import Cookie, FastAPI
from pydantic import BaseModel

app = FastAPI()


@app.get("/items/")
async def read_items(ads_id: Annotated[str, Cookie()]) -> dict[str, str]:
    """Path operation for the GET items endpoint."""
    return {"ads_id (Cookie)": ads_id}


class Cookies(BaseModel):
    """Pydantic model for cookies."""

    session_id: str
    app1_tracker: str | None = None
    app2_tracker: str | None = None

    model_config = {"extra": "forbid"}


@app.get("/v2/items/")
async def read_items_v2(cookies: Annotated[Cookies, Cookie()]) -> dict[str, str | None]:
    """Path operation for the GET items endpoint."""
    return {**cookies.model_dump()}


@app.get("/v3/items/")
async def read_items_v3(cookies: Annotated[Cookies, Cookie()]) -> dict[str, str | None]:
    """Path operation for the GET items endpoint."""
    return {**cookies.model_dump()}
