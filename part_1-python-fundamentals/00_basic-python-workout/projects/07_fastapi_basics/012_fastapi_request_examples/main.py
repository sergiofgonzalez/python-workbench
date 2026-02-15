"""Illustrates how to add request and field examples."""

from typing import Annotated

from fastapi import Body, FastAPI
from pydantic import BaseModel, Field

app = FastAPI()


class Item(BaseModel):
    """Pydantic model for an item."""

    name: str
    description: str | None = None
    price: float
    tax: float | None = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Example Item",
                    "description": "This is an example item",
                    "price": 10.5,
                    "tax": 1.5,
                },
                {
                    "name": "Example Item",
                    "price": 10.5,
                },
            ],
        },
    }


@app.post("/items/{item_id}")
async def create_item(item_id: int, item: Item) -> dict[str, str | int | float | None]:
    """Path operation for the POST endpoint to create an item."""
    return {"item_id": item_id, **item.model_dump()}


class ItemV2(BaseModel):
    """Pydantic model for an item."""

    name: str
    description: Annotated[str | None, Field(example="A very nice item")] = None
    price: float
    tax: float | None = None


@app.post("/v2/items/{item_id}")
async def create_item_v2(
    item_id: int,
    item: ItemV2,
) -> dict[str, str | int | float | None]:
    """Path operation for the POST endpoint to create an item."""
    return {"item_id": item_id, **item.model_dump()}


class ItemV3(BaseModel):
    """Pydantic model for an item."""

    name: str
    description: str | None = None
    price: float
    tax: float | None = None


@app.post("/v3/items/{item_id}")
async def create_item_v3(
    item_id: int,
    item: Annotated[
        ItemV3,
        Body(
            examples=[
                {
                    "name": "Example Item",
                    "description": "This is an example item",
                    "price": 10.5,
                    "tax": 1.5,
                },
                {
                    "name": "Example Item",
                    "price": 10.5,
                },
            ],
        ),
    ],
) -> dict[str, str | int | float | None]:
    """Path operation for the POST endpoint to create an item."""
    return {"item_id": item_id, **item.model_dump()}


@app.post("/v4/items/{item_id}")
async def create_item_v4(
    item_id: int,
    item: Annotated[
        ItemV3,
        Body(
            openapi_examples={
                "normal": {
                    "summary": "A normal example",
                    "description": "A **normal** item works correctly.",
                    "value": {
                        "name": "Foo",
                        "description": "A very nice Item",
                        "price": 35.4,
                        "tax": 3.2,
                    },
                },
                "simple": {
                    "summary": "A simple example",
                    "description": "A **simple** item works correctly.",
                    "value": {
                        "name": "Foo",
                        "price": 35.4,
                    },
                },
            },
        ),
    ],
) -> dict[str, str | int | float | None]:
    """Path operation for the POST endpoint to create an item."""
    return {"item_id": item_id, **item.model_dump()}
