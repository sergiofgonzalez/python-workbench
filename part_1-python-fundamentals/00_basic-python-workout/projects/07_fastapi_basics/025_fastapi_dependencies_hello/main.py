"""Illustrates the basics of FastAPI Dependency Injection."""

from typing import Annotated

from fastapi import Depends, FastAPI

app = FastAPI()


async def common_parameters(
    q: str | None = None,
    skip: int = 0,
    limit: int = 100,
) -> dict[str, str | int | None]:
    """A dependency function that can be shared across multiple path operations."""
    return {"q": q, "skip": skip, "limit": limit}


# Initial version without type aliases:
# @app.get("/items/")
# async def read_items(
#     commons: Annotated[dict[str, str | int | None], Depends(common_parameters)],
# ) -> dict[str, str | int | None]:
#     """Path operation for the GET /items/ endpoint."""
#     return {"operation": "read_items", **commons}  # noqa: ERA001


# @app.get("/users/")
# async def read_users(
#     commons: Annotated[dict[str, str | int | None], Depends(common_parameters)],
# ) -> dict[str, str | int | None]:
#     """Path operation for the GET /users/ endpoint."""
#     return {"operation": "read_users", **commons}  # noqa: ERA001

# Refactored version with type aliases:
CommonParams = Annotated[dict[str, str | int | None], Depends(common_parameters)]


@app.get("/items/")
async def read_items(
    commons: CommonParams,
) -> dict[str, str | int | None]:
    """Path operation for the GET /items/ endpoint."""
    return {"operation": "read_items", **commons}


@app.get("/users/")
async def read_users(
    commons: CommonParams,
) -> dict[str, str | int | None]:
    """Path operation for the GET /users/ endpoint."""
    return {"operation": "read_users", **commons}
