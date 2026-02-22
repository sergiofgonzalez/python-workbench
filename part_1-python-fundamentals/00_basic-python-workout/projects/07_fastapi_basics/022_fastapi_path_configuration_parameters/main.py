"""Illustrates the basics of path configuration."""

from fastapi import FastAPI, status
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    """Represents an item with a name and an optional description."""

    name: str
    description: str | None = None


@app.post("/items/", status_code=status.HTTP_201_CREATED)
async def create_item(item: Item) -> Item:
    """Path operation for creating an item."""
    return item


@app.get("/v1/items/", tags=["items"])
async def read_items() -> list[Item]:
    """Path operation for reading items."""
    return [
        Item(name="Item 1", description="The first item"),
        Item(name="Item 2", description="The second item"),
    ]


@app.post("/v1/items/", status_code=status.HTTP_201_CREATED, tags=["items"])
async def create_item_v1(item: Item) -> Item:
    """Path operation for creating an item."""
    return item


@app.get("/v1/users/", tags=["users"])
async def read_users() -> list[str]:
    """Path operation for reading users."""
    return ["User 1", "User 2"]


@app.post(
    "/v2/items/",
    summary="Create an item (v2)",
    description="This endpoint allows you to create an item using version 2 of the API.",  # noqa: E501
)
async def create_item_v2(item: Item) -> Item:
    """Path operation for creating an item."""
    return item


@app.post(
    "/v3/items/",
    summary="Create an item (v3)",
)
async def create_item_v3(item: Item) -> Item:
    """Path operation for creating an item.

    Args:
        item (Item): The item to create.

    Returns:
        Item: The created item.
    """
    return item

@app.post(
    "/v4/items/",
    summary="Create an item (v4)",
    deprecated=True,
)
async def create_item_v4(item: Item) -> Item:
    """Path operation for creating an item.

    Args:
        item (Item): The item to create.

    Returns:
        Item: The created item.
    """
    return item
