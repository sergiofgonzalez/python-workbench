"""Illustrates the basics of FastAPI testing without /test dirs."""

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def read_root() -> dict[str, str]:
    """Path operation for the GET root endpoint."""
    return {"message": "Hello, world!"}
