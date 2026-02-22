"""Illustrates the basics of HTTP error handling with FastAPI."""
import stat

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exception_handlers import (
    http_exception_handler as fastapi_http_exception_handler,
)
from fastapi.exception_handlers import (
    request_validation_exception_handler as fastapi_request_validation_exception_handler,
)
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, PlainTextResponse
from pydantic import BaseModel
from starlette.exceptions import HTTPException as StarletteHTTPException

app = FastAPI()


items = {"foo": "bar"}


@app.get("/items/{item_id}")
async def read_item(item_id: str) -> dict[str, str]:
    """Path operation for the GET item endpoint."""
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"item": items[item_id]}


@app.get("/v2/items/{item_id}")
async def read_item_v2(item_id: str) -> dict[str, str]:
    """Path operation for the GET item endpoint."""
    if item_id not in items:
        raise HTTPException(
            status_code=404,
            detail="Item not found",
            headers={"X-Error": f"The item {item_id} was not found"},
        )
    return {"item": items[item_id]}


class MyCustomError(Exception):
    """Custom exception class."""

    def __init__(self, name: str) -> None:
        """Initialize the exception with a name."""
        self.name = name


@app.exception_handler(MyCustomError)
async def my_custom_error_handler(request: Request, exc: MyCustomError) -> JSONResponse:
    """Custom exception handler for MyCustomError."""
    return JSONResponse(
        status_code=418,
        content={
            "message": f"Oops! {exc.name} did something. There goes a teapot.",
            "request_url": str(request.url),
        },
    )


@app.get("/v3/items/{item_id}")
async def read_item_v3(item_id: int) -> dict[str, int]:
    """Path operation for the GET item endpoint."""
    if item_id == 3:  # noqa: PLR2004
        raise MyCustomError(name=f"Item {item_id}")
    return {"item_id": item_id}


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
) -> PlainTextResponse:
    """Custom exception handler for request validation errors."""
    message = "Validation errors:\n"
    for error in exc.errors():
        message += f"Field: {error['loc']}: {error['msg']}\n"
    message += f"on request: {request.method} {request.url}"
    return PlainTextResponse(
        status_code=422,
        content=message,
    )


@app.get("/v4/items/{item_id}")
async def read_item_v4(item_id: int) -> dict[str, int]:
    """Path operation for the GET item endpoint."""
    return {"item_id": item_id}


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(
    request: Request,
    exc: HTTPException,
) -> PlainTextResponse:
    """Custom exception handler for HTTP exceptions."""
    return PlainTextResponse(
        status_code=exc.status_code,
        content=f"HTTP error occurred: {exc} when accessing {request.method} {request.url}",
    )


@app.get("/v5/items/{item_id}")
async def read_item_v5(item_id: int) -> dict[str, int]:
    """Path operation for the GET item endpoint."""
    if item_id == 3:  # noqa: PLR2004
        raise HTTPException(status_code=418, detail="This is a teapot for item 3")
    return {"item_id": item_id}


class Item(BaseModel):
    """Pydantic model for an item."""

    title: str
    size: int


@app.exception_handler(RequestValidationError)
async def validation_exception_handler_v6(
    request: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    """Custom exception handler for request validation errors."""
    return JSONResponse(
        status_code=422,
        content={
            "detail": exc.errors(),
            "body": exc.body,
            "endpoint": f"{request.method} {request.url}",
        },
    )


@app.post("/v6/items/")
async def read_item_v6(item: Item) -> Item:
    """Path operation for the POST item endpoint."""
    return item


@app.exception_handler(RequestValidationError)
async def validation_exception_handler_v7(
    request: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    """Custom exception handler for request validation errors."""
    print(f"Validation error: {exc} for request {request.method} {request.url}")
    await fastapi_request_validation_exception_handler(request, exc)


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler_v7(
    request: Request,
    exc: HTTPException,
) -> PlainTextResponse:
    """Custom exception handler for HTTP exceptions."""
    print(f"HTTP error occurred: {exc} when accessing {request.method} {request.url}")
    await fastapi_http_exception_handler(request, exc)


@app.get("/v7/items/{item_id}")
async def read_item_v7(item_id: int) -> dict[str, int]:
    """Path operation for the GET item endpoint."""
    if item_id == 3:  # noqa: PLR2004
        raise HTTPException(status_code=418, detail=">>> This is a teapot for item 3")
    return {"item_id": item_id}
