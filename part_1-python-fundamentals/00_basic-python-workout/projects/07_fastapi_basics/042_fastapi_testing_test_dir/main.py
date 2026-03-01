"""Illustrates the basics of FastAPI testing when using a /test dir."""

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def read_root() -> dict[str, str]:
    """Path operation for the GET root endpoint."""
    return {"message": "Hello, world!"}
