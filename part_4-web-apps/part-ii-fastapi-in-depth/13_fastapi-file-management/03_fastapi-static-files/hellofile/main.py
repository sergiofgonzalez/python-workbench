"""
Entry point for the web application
"""

import os
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Get directory on which main.py is located
BASE_DIR = Path(__file__).resolve().parent


# Mount the static directory to the root of the web application
app.mount(
    "/public",
    StaticFiles(directory=BASE_DIR / "public", html=True),
    name="public",
)


@app.get("/")
def read_root() -> str:
    return "Hello, world!"


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", reload=True, port=int(os.getenv("PORT", "8080")))
