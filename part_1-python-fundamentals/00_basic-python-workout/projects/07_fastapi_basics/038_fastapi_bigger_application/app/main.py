"""main application and entry point for the bigger FastAPI app."""

from fastapi import Depends, FastAPI

from .dependencies import get_token_from_header, get_token_from_query
from .internal import admin
from .routers import items, users

app = FastAPI(dependencies=[Depends(get_token_from_query)])

app.include_router(items.router)
app.include_router(users.router)
app.include_router(
    admin.router,
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(get_token_from_header)],
    responses={418: {"description": "I'm a teapot"}},
)


@app.get("/")
async def read_root() -> dict[str, str]:
    """Path operation for the GET root endpoint."""
    return {"message": "Hello, world from a bigger FastAPI app!"}
