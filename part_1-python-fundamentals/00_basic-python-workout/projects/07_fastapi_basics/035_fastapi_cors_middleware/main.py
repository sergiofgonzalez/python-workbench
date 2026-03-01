"""Illustrates how to use FastAPI's CORSMiddleware."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,  # ty:ignore[invalid-argument-type]
    allow_origins=["http://localhost", "http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


@app.get("/")
async def read_root() -> dict[str, str]:
    """Path operation for the GET root endpoint."""
    return {"message": "Hello, world!"}
