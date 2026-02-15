"""Illustrates how to use multiple body parameters."""

from typing import Annotated

from fastapi import Body, FastAPI, Path
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    """Pydantic model for an item."""

    name: str
    description: str | None = None
    price: float
    tax: float | None = None


@app.put("/items/{item_id}")
async def read_item(
    item_id: Annotated[int, Path(title="Item ID", ge=0, le=1000)],
    q: str | None = None,
    item: Item = None,
) -> dict[str, str | int | Item | None]:
    """Path operation for reading an item."""
    result = {"item_id": item_id}
    if item:
        result.update({"item": item})
    if q:
        result.update({"q": q})
    return result


class ItemV2(BaseModel):
    """Pydantic model for an item."""

    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: list[str] = []


class User(BaseModel):
    """Pydantic model for a user."""

    username: str
    full_name: str | None = None


@app.post("/items/{item_id}")
async def create_item(
    item_id: int,
    item: ItemV2,
    user: User,
) -> dict[str, int | ItemV2 | User]:
    """Path operation with two body parameters."""
    return {"item_id": item_id, "item": item, "user": user}


@app.post("/v2/items/{item_id}")
async def create_item_v2(
    item_id: int,
    item: ItemV2,
    user: User,
    importance: Annotated[int, Body()],
) -> dict[str, int | ItemV2 | User]:
    """Path operation with two body parameters and an additional body parameter."""
    return {"item_id": item_id, "item": item, "user": user, "importance": importance}


@app.post("/v3/items/{item_id}")
async def create_item_v3(
    item_id: int,
    item: ItemV2,
    user: User,
    importance: Annotated[int, Body()],
    q: str | None = None,
) -> dict[str, int | ItemV2 | User | str]:
    """Path operation with two body parameters and an additional body parameter."""
    result = {"item_id": item_id, "item": item, "user": user, "importance": importance}
    if q:
        result.update({"q": q})
    return result


@app.post("/v4/items/{item_id}")
async def create_item_v4(
    item_id: int,
    item: Annotated[Item, Body(embed=True)],
) -> dict[str, int | Item]:
    """Path operation with two body parameters and an additional body parameter."""
    result = {"item_id": item_id, "item": item}
    return result  # noqa: RET504
