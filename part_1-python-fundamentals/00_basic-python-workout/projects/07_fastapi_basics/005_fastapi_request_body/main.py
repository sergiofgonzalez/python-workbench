"""Illustrates the basics of FastAPI request body management."""

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    """Pydantic model for an item."""

    name: str
    description: str | None = None
    price: float
    tax: float | None = None


@app.post("/items/")
async def create_item(item: Item) -> Item:
    """Path operation for creating an item."""
    return item


@app.put("/items/{item_id}")
async def update_item(
    item_id: int,
    item: Item,
    q: str | None = None,
) -> dict[str, str | float | int | None]:
    """Path operation for updating an item."""
    results = {"item_id": item_id, "name": item.name, **item.model_dump()}
    if q:
        results.update({"q": q})
    return results


@app.post("/v2/items/")
async def create_item_v2(item: Item) -> dict[str, str | int | float | None]:
    """Path operation for creating an item with a different response model."""
    item_dict = item.model_dump()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict
