"""Illustrates how to use PUT and PATCH for updates."""

from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    """Represents an item in the inventory."""

    name: str | None = None
    description: str | None = None
    price: float
    tax: float | None = None
    tags: list[str] = []


items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
    "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
}


@app.get("/items/{item_id}")
async def read_item(item_id: str) -> Item:
    """Path operation for the GET item endpoint."""
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return items[item_id]


@app.put("/items/{item_id}")
async def update_item(item_id: str, item: Item) -> Item:
    """Path operation for the PUT item endpoint."""
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    items[item_id] = jsonable_encoder(item)
    return items[item_id]

@app.patch("/items/{item_id}")
async def update_item_partial(item_id: str, item: Item) -> Item:
    """Path operation for the PATCH item endpoint."""
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    stored_item_data = items[item_id]
    stored_item_model = Item(**stored_item_data)
    update_data = item.model_dump(exclude_unset=True)
    updated_item = stored_item_model.copy(update=update_data)
    items[item_id] = jsonable_encoder(updated_item)
    return items[item_id]