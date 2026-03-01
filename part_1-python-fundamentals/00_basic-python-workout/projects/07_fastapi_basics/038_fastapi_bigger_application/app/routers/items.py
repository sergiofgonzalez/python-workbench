"""Items module in routers sub-package: item management path operations."""

from fastapi import APIRouter, Depends, HTTPException

from ..dependencies import get_token_from_header  # noqa: TID252

router = APIRouter(
    prefix="/items",
    tags=["items"],
    dependencies=[Depends(get_token_from_header)],
    responses={404: {"description": "Not found"}},
)

fake_items_db = {
    "item1": {"name": "Foo"},
    "item2": {"name": "Bar"},
    "item3": {"name": "Baz"},
}


@router.get("/")
async def read_items() -> dict[str, dict[str, str]]:
    """Path operation for the GET /items/ endpoint."""
    return fake_items_db


@router.get("/{item_id}")
async def read_item(item_id: str) -> dict[str, str]:
    """Path operation for the GET /items/{item_id} endpoint."""
    if item_id not in fake_items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return fake_items_db[item_id]


@router.put(
    "/{item_id}",
    tags=["custom"],
    responses={403: {"description": "Operation forbidden"}},
)
async def update_item(item_id: str, item: dict[str, str]) -> dict[str, str]:
    """Path operation for the PUT /items/{item_id} endpoint."""
    if item_id not in fake_items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    if item_id == "item3":
        raise HTTPException(status_code=403, detail="Operation forbidden for item3")
    fake_items_db[item_id] = item
    return item
