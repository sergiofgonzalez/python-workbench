"""Illustrates the basics of FastAPI testing when using a /test dir."""

from typing import Annotated

from fastapi import FastAPI, Header, HTTPException, status
from pydantic import BaseModel

app = FastAPI()

fake_secret_token = "***"  # noqa: S105

fake_db = {
    "foo": {"id": "foo", "title": "Foo", "description": "The Foo item"},
    "bar": {"id": "bar", "title": "Bar", "description": "The Bar item"},
}


class Item(BaseModel):
    """Pydantic model for an item."""

    id: str
    title: str
    description: str | None = None


@app.get("/items/{item_id}")
async def read_item(item_id: str, x_token: Annotated[str, Header()]) -> Item:
    """Path operation for the GET item endpoint."""
    if x_token != fake_secret_token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid X-Token header",
        )
    if item_id not in fake_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found",
        )
    return fake_db[item_id]  # ty:ignore[invalid-return-type]


@app.post("/items/")
async def create_item(item: Item, x_token: Annotated[str, Header()]) -> Item:
    """Path operation for the POST item endpoint."""
    if x_token != fake_secret_token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid X-Token header",
        )
    if item.id in fake_db:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Item already exists",
        )
    fake_db[item.id] = item.model_dump()
    return item
