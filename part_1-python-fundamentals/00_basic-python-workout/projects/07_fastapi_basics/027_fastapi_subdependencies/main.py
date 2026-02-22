"""Illustrates the basics of FastAPI subdependencies."""

import random
from typing import Annotated

from fastapi import Cookie, Depends, FastAPI

app = FastAPI()


async def query_extractor(q: str | None = None) -> str | None:
    """Extracts the query parameter `q`."""
    return q


async def query_or_cookie_extractor(
    q: Annotated[str | None, Depends(query_extractor)] = None,
    last_query: Annotated[str | None, Cookie()] = None,
) -> str | None:
    """Extracts the query parameter `q` or the cookie `last_query`."""
    if not q:
        return last_query
    return q


@app.get("/items/")
async def read_items(
    q_or_last_query_cookie: Annotated[
        str | None,
        Depends(query_or_cookie_extractor),
    ] = None,
) -> dict[str, str | None]:
    """Path operation for the GET /items/ endpoint."""
    return {"q_or_last_query_cookie": q_or_last_query_cookie}


# sub-dependencies cache
# This was not initially working for me, as I was applying the `use_cache=False`
# parameter to the wrong dependencies. The `use_cache=False` parameter should be
# applied to the dependencies that are used as sub-dependencies, not to the
# dependencies that are used as path operation dependencies.


async def get_random_item_id() -> int:
    """Returns a random item ID."""
    rand_value = random.randint(1, 1000)  # noqa: S311
    return rand_value  # noqa: RET504


async def get_rand_item(item_id: Annotated[int, Depends(get_random_item_id)]) -> str:
    """Returns the item ID."""
    return f"item_id={item_id}"


async def get_other_rand_item(
    item_id: Annotated[int, Depends(get_random_item_id)],
) -> str:
    """Returns the item ID."""
    return f"other_item_id={item_id}"


@app.get("/cached/items/")
async def read_items_cached(
    q1: Annotated[str, Depends(get_rand_item)],
    q2: Annotated[str, Depends(get_other_rand_item)],
) -> dict[str, str]:
    """Path operation for the GET /cached/items/ endpoint."""
    return {"q1": q1, "q2": q2}


async def get_rand_item_no_cache(
    item_id: Annotated[int, Depends(get_random_item_id, use_cache=False)],
) -> str:
    """Returns the item ID without dependency caching."""
    return f"item_id={item_id}"


async def get_other_rand_item_no_cache(
    item_id: Annotated[int, Depends(get_random_item_id, use_cache=False)],
) -> str:
    """Returns the other item ID without dependency caching."""
    return f"other_item_id={item_id}"


@app.get("/no-cached/items/")
async def read_items_nocached(
    q1: Annotated[str, Depends(get_rand_item_no_cache)],
    q2: Annotated[str, Depends(get_other_rand_item_no_cache)],
) -> dict[str, str]:
    """Path operation for the GET /no-cached/items/ endpoint."""
    return {"q1": q1, "q2": q2}
