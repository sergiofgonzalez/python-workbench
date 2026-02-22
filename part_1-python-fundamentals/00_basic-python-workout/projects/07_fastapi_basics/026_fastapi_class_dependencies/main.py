"""Illustrates the basics of implementing dependencies with classes."""

from typing import Annotated

from fastapi import Depends, FastAPI

app = FastAPI()


fake_items_db = [
    {"item_name": "Foo"},
    {"item_name": "Bar"},
    {"item_name": "Baz"},
    {"item_name": "Qux"},
    {"item_name": "Quux"},
    {"item_name": "Corge"},
    {"item_name": "Grault"},
]


class CommonQueryParams:
    """A class to represent common query parameters."""

    def __init__(self, q: str | None = None, skip: int = 0, limit: int = 100) -> None:
        """Initialize the CommonQueryParams instance."""
        self.q = q
        self.skip = skip
        self.limit = limit


@app.get("/items/")
async def read_items(
    commons: Annotated[CommonQueryParams, Depends(CommonQueryParams)],
) -> dict[str, str | int | None | list[dict[str, str]]]:
    """Path operation for the GET root endpoint."""
    response = {}
    if commons.q:
        response.update({"q": commons.q})
    response.update({"skip": commons.skip})
    response.update({"limit": commons.limit})
    response.update(
        {"items": fake_items_db[commons.skip : commons.skip + commons.limit]},
    )
    return response
