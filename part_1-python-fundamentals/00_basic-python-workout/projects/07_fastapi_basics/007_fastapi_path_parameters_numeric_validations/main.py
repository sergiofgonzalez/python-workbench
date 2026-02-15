"""Illustrates how to apply numeric validations to path parameters."""

from typing import Annotated

from fastapi import FastAPI, Path, Query

app = FastAPI()


@app.get("/items/{item_id}")
async def read_item(
    item_id: Annotated[int, Path(description="Item ID", ge=1)],
    q: Annotated[str | None, Query(alias="item-query")] = None,
    pct_discount: Annotated[float, Query(ge=0.0, le=100.0)] = 0.0,
) -> dict[str, int | str | float | None]:
    """Path operation for the GET item endpoint."""
    data = {"item_id": item_id}
    if q:
        data.update({"q": q})
    if pct_discount:
        data.update({"pct_discount": pct_discount})
    return data
