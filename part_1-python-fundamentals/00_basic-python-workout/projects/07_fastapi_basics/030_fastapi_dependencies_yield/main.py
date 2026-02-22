"""Illustrates how to implement dependencies with yield in FastAPI."""

from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException

app = FastAPI()


fake_items_db = {
    "foo": {"name": "foo", "owner": "Alice"},
    "bar": {"name": "bar", "owner": "Bob"},
    "baz": {"name": "baz", "owner": "Charlie"},
}


class OwnerError(Exception):
    """Custom exception for unauthorized access to items."""


async def get_username() -> AsyncGenerator[str, None]:
    """Simulates a dependency that retrieves the username."""
    try:
        # Simulate some processing, e.g., authentication
        yield "Alice"
        print("Cleanup after yielding the username")
    except OwnerError as e:
        raise HTTPException(
            status_code=400,
            detail="Invalid owner for the requested item",
        ) from e
    except HTTPException:
        raise


@app.get("/items/{item_id}")
async def read_item(
    item_id: str,
    username: Annotated[str, Depends(get_username)],
) -> dict[str, str]:
    """Path operation for the GET item endpoint."""
    if item_id not in fake_items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    if fake_items_db[item_id]["owner"] != username:
        raise OwnerError
    return fake_items_db[item_id]
