"""Illustrates the basics of FastAPI's middleware system."""

import time
from collections.abc import Awaitable, Callable

from fastapi import FastAPI, Request, Response
from pydantic import BaseModel

app = FastAPI()


@app.middleware("http")
async def add_process_time_header(
    request: Request,
    call_next: Callable[[Request], Awaitable[Response]],
) -> Response:
    """Middleware function that adds a custom header to the response."""
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


@app.middleware("http")
async def log_request(
    request: Request,
    call_next: Callable[[Request], Awaitable[Response]],
) -> Response:
    """Middleware function that logs the incoming request."""
    body = await request.body()
    print(
        f"Received request: {request.method} {request.url} with body: {body.decode('utf-8')}",
    )
    response = await call_next(request)
    print(f"Response status: {response.status_code}")
    return response


@app.get("/items/")
async def read_items() -> list[dict[str, str]]:
    """Path operation for the GET /items/ endpoint."""
    return [{"item_id": "Foo"}, {"item_id": "Bar"}, {"item_id": "Baz"}]


class Item(BaseModel):
    """Pydantic model for an item."""

    item_id: str


@app.post("/items/")
async def create_item(item: Item) -> Item:
    """Path operation for the POST /items/ endpoint."""
    return item
