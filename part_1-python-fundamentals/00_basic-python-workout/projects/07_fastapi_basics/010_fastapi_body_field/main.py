"""Illustrates the basics of Field for body parameters."""
from typing import Annotated

from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()


class Item(BaseModel):
    """Model for an item."""

    name: str
    description: Annotated[str | None, Field(
        title="Description of the item",
        max_length=3,
    )] = None
    price: Annotated[float, Field(
        gt=0, description="Price of the item (must be greater than zero)",
    )]
    tax: float | None = None


@app.put("/items/{item_id}")
async def read_item(item_id: int, item: Item) -> dict[str, int | Item]:
    """Path operation for the GET root endpoint."""
    return {"item_id": item_id, "item": item}
