"""Illustrates how to apply string validations to query parameters."""

import random
from typing import Annotated

from fastapi import FastAPI, Query
from pydantic import AfterValidator

app = FastAPI()


@app.get("/items/")
async def read_items(
    q: Annotated[str | None, Query(max_length=50)] = None,
) -> dict[str, list[dict[str, str]] | str | None]:
    """Path operation for the GET root endpoint."""
    data = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        return {**data, "q": q}
    return data


@app.get("/v2/items/")
async def read_items_v2(
    q: Annotated[
        str | None,
        Query(min_length=3, max_length=50, pattern=r"^\d+$"),
    ] = None,
) -> dict[str, list[dict[str, str]] | str | None]:
    """Path operation for the GET root endpoint."""
    data = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        return {**data, "q": q}
    return data


@app.get("/v3/items/")
async def read_items_v3(
    q: Annotated[
        str | None,
        Query(min_length=3, max_length=50, pattern=r"^\d+$"),
    ] = "012345",
) -> dict[str, list[dict[str, str]] | str | None]:
    """Path operation for the GET root endpoint."""
    data = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        return {**data, "q": q}
    return data


@app.get("/v4/items/")
async def read_items_v4(
    q: Annotated[
        str,
        Query(min_length=3),
    ],
) -> dict[str, list[dict[str, str]] | str | None]:
    """Path operation for the GET root endpoint."""
    data = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        return {**data, "q": q}
    return data


@app.get("/v5/items/")
async def read_items_v5(
    q: Annotated[list[str] | None, Query()] = None,
) -> dict[str, list[dict[str, str]] | list[str] | None]:
    """Path operation for the GET root endpoint."""
    data = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        return {**data, "q": q}
    return data


@app.get("/v6/items/")
async def read_items_v6(
    q: Annotated[list[str] | None, Query()] = ["1", "2", "3"],  # noqa: B006
) -> dict[str, list[dict[str, str]] | list[str] | None]:
    """Path operation for the GET root endpoint."""
    data = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        return {**data, "q": q}
    return data


@app.get("/v7/items/")
async def read_items_v7(
    q: Annotated[
        str | None,
        Query(
            min_length=3,
            max_length=10,
            title="Query string",
            description="Query string for the items to search in the db",
        ),
    ] = None,
) -> dict[str, list[dict[str, str]] | str | None]:
    """Path operation for the GET root endpoint."""
    data = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        return {**data, "q": q}
    return data


@app.get("/v8/items/")
async def read_items_v8(
    q: Annotated[
        str | None,
        Query(
            min_length=3,
            max_length=10,
            alias="item-query",
        ),
    ] = None,
) -> dict[str, list[dict[str, str]] | str | None]:
    """Path operation for the GET root endpoint."""
    data = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        return {**data, "q": q}
    return data


@app.get("/v9/items/")
async def read_items_v9(
    q: Annotated[
        str | None,
        Query(
            min_length=3,
            max_length=10,
            deprecated=True,
        ),
    ] = None,
) -> dict[str, list[dict[str, str]] | str | None]:
    """Path operation for the GET root endpoint."""
    data = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        return {**data, "q": q}
    return data


@app.get("/v10/items/")
async def read_items_v10(
    hidden_query: Annotated[
        str | None,
        Query(
            min_length=3,
            max_length=10,
            include_in_schema=False,
        ),
    ] = None,
) -> dict[str, list[dict[str, str]] | str | None]:
    """Path operation for the GET root endpoint."""
    data = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if hidden_query:
        return {**data, "hidden_query": hidden_query}
    return {**data, "hidden_query": "Not found"}


def check_valid_id(item_id: str) -> str:
    """Checks if the provided ID is valid."""
    if not item_id.startswith(("isbn-", "imdb-")):
        msg = "Invalid ID format. ID must start with 'isbn-' or 'imdb-'."
        raise ValueError(msg)
    return item_id


@app.get("/v11/items/")
async def read_items_v11(
    item_id: Annotated[str | None, AfterValidator(check_valid_id)] = None,
) -> dict[str, list[dict[str, str]] | str | None]:
    """Path operation for the GET root endpoint."""
    data = {
        "isbn-9781529046137": "The Hitchhiker's Guide to the Galaxy",
        "imdb-tt0371724": "The Hitchhiker's Guide to the Galaxy",
        "isbn-9781439512982": "Isaac Asimov: The Complete Stories, Vol. 2",
    }
    if item_id and item_id in data:
        return {data[item_id]: data[item_id]}

    item_id, item_name = random.choice(list(data.items()))  # noqa: S311
    return {item_id: item_name}


@app.get("/v12/items/")
async def read_items_v12(
    q: Annotated[
        str | None,
        Query(max_length=10),
    ],
) -> dict[str, list[dict[str, str]] | str | None]:
    """Path operation for the GET root endpoint."""
    data = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        return {**data, "q": q}
    return data
