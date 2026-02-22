"""Illustrates the basics of forms with FastAPI."""

from typing import Annotated

from fastapi import FastAPI, Form
from pydantic import BaseModel

app = FastAPI()


@app.post("/login")
async def login(
    username: Annotated[str, Form()],
    password: Annotated[str, Form()],
) -> dict[str, str]:
    """Path operation for the POST login endpoint."""
    return {"username": username, "password": password}


class FormData(BaseModel):
    """Pydantic model for form data."""

    username: str
    password: str


@app.post("/v2/login")
async def login_v2(form_data: Annotated[FormData, Form()]) -> FormData:
    """Path operation for the POST login endpoint."""
    return form_data


class FormDataV2(BaseModel):
    """Pydantic model for form data."""

    username: str
    password: str

    model_config = {"extra": "forbid"}


@app.post("/v3/login")
async def login_v3(form_data: Annotated[FormDataV2, Form()]) -> FormDataV2:
    """Path operation for the POST login endpoint."""
    return form_data
