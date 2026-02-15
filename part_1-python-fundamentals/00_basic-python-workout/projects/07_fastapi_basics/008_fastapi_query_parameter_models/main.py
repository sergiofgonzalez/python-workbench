"""Illustrates how to use Pydantic models for query parameters."""

from typing import Annotated, Literal

from fastapi import FastAPI, Query
from pydantic import BaseModel, Field

app = FastAPI()


class FilterParams(BaseModel):
    """Reusable Pydantic model for query parameters."""

    limit: int = Field(default=100, ge=0, le=100)
    offset: int = Field(default=0, ge=0)
    order_by: Literal["created_at", "updated_at"] = "created_at"
    tags: list[str] = []


@app.get("/items/")
async def read_items(
    filter_query: Annotated[FilterParams, Query()],
) -> dict[str, FilterParams]:
    """Path operation for the GET root endpoint."""
    return {"q": filter_query}


class FilterParamsV2(BaseModel):
    """Reusable Pydantic model for query parameters that prevents extra params."""

    model_config = {"extra": "forbid"}

    limit: int = Field(default=100, ge=0, le=100)
    offset: int = Field(default=0, ge=0)
    order_by: Literal["created_at", "updated_at"] = "created_at"
    tags: list[str] = []


@app.get("/v2/items/")
async def read_items_v2(
    filter_query: Annotated[FilterParamsV2, Query()],
) -> dict[str, FilterParamsV2]:
    """Path operation for the GET root endpoint."""
    return {"q": filter_query}
