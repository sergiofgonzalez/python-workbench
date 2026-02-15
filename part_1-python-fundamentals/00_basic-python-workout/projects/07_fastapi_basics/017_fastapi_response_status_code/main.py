"""Illustrates the basics of FastAPI response status code."""

from http import HTTPStatus

from fastapi import FastAPI, status

app = FastAPI()


@app.post("/items/", status_code=201)
async def create_item() -> dict[str, str]:
    """Path operation for creating an item."""
    return {"message": "Item created successfully!"}


@app.post("/v2/items/", status_code=HTTPStatus.CREATED)
async def create_item_v2() -> dict[str, str | HTTPStatus]:
    """Path operation for creating an item."""
    return {"message": "Item created successfully!", "status_code": HTTPStatus.CREATED}


@app.post("/v3/items/", status_code=status.HTTP_201_CREATED)
async def create_item_v3() -> dict[str, str]:
    """Path operation for creating an item."""
    return {"message": "Item created successfully!"}
