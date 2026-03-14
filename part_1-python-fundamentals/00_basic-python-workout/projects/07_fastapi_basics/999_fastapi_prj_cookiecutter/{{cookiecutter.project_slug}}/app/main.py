"""Main application entry point."""

from fastapi import FastAPI

from app.routers import greetings

app = FastAPI()

app.include_router(greetings.router)


@app.get("/")
async def read_root() -> dict[str, str]:
    """Path operation for the GET root endpoint."""
    return {"message": "Hello, world!"}
