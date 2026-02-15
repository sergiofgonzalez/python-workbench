"""Illustrates the basics of nested models for request bodies in FastAPI."""

from fastapi import FastAPI
from pydantic import BaseModel, HttpUrl

app = FastAPI()


class Item(BaseModel):
    """Model for an item."""

    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: list[str] = []


@app.put("/items/{item_id}")
async def read_item(item_id: int, item: Item) -> dict[str, int | Item]:
    """Path operation for the GET root endpoint."""
    results = {"item_id": item_id, "item": item}
    return results  # noqa: RET504


class ItemV2(BaseModel):
    """Model for an item."""

    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set()


@app.put("/v2/items/{item_id}")
async def read_item_v2(item_id: int, item: ItemV2) -> dict[str, int | ItemV2]:
    """Path operation for the GET root endpoint."""
    results = {"item_id": item_id, "item": item}
    return results  # noqa: RET504


class Image(BaseModel):
    """Model for an image."""

    url: HttpUrl
    name: str


class ItemV3(BaseModel):
    """Model for an item."""

    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set()
    image: Image | None = None


@app.put("/v3/items/{item_id}")
async def read_item_v3(item_id: int, item: ItemV3) -> dict[str, int | ItemV3]:
    """Path operation for the GET root endpoint."""
    results = {"item_id": item_id, "item": item}
    return results  # noqa: RET504


class ItemV4(BaseModel):
    """Model for an item."""

    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set()
    images: list[Image] = []


@app.put("/v4/items/{item_id}")
async def read_item_v4(item_id: int, item: ItemV4) -> dict[str, int | ItemV4]:
    """Path operation for the GET root endpoint."""
    results = {"item_id": item_id, "item": item}
    return results  # noqa: RET504


class Offer(BaseModel):
    """Model for an offer."""

    name: str
    description: str | None = None
    price: float
    items: list[ItemV4] = []


@app.post("/offers/")
async def create_offer(offer: Offer) -> Offer:
    """Path operation for the POST offers endpoint."""
    return offer


@app.post("/images/multiple/")
async def create_multiple_images(images: list[Image]) -> list[Image]:
    """Path operation for the POST images/multiple endpoint."""
    return images


@app.post("/index-weights/")
async def create_index_weights(weights: dict[int, float]) -> dict[int, float]:
    """Path operation for the POST index-weights endpoint."""
    return weights
