"""Illustrates the basics of FastAPI's jsonable encoder."""

from datetime import datetime

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    """Pydantic model for an item."""

    title: str
    description: str | None = None
    timestamp: datetime


fake_db = {}


@app.put("/items/{item_id}")
async def upsert_item(item_id: str, item: Item) -> dict[str, str | None | datetime]:
    """Path operation for upserting an item."""
    item_data = jsonable_encoder(item)
    fake_db[item_id] = item_data
    return item_data
