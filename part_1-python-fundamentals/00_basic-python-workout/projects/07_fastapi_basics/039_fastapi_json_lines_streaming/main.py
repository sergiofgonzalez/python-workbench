"""Illustrates how to stream JSON lines from FastAPI."""

from collections.abc import AsyncIterable, Iterable

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    """Pydantic model for an item."""

    name: str
    description: str | None = None


items = [
    Item(name="Item 1", description="This is item 1"),
    Item(name="Item 2", description="This is item 2"),
    Item(name="Item 3", description="This is item 3"),
]


@app.get("/items/stream")
async def stream_items() -> AsyncIterable[Item]:
    """Path operation for the GET root endpoint."""
    for item in items:
        yield item


@app.get("/items/stream-sync")
def stream_items_sync() -> Iterable[Item]:
    """Path operation for the GET root endpoint."""
    yield from items
