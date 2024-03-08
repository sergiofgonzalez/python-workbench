"""
Entry point for the web application
"""

import os
from typing import Generator

from fastapi import FastAPI
from fastapi.responses import FileResponse, StreamingResponse
from pathlib import Path

app = FastAPI()


@app.get("/download-small-file/{name}")
async def download_small_file(name: str) -> FileResponse:
    return FileResponse(f"./data/{name}")


def generator_file(file_path: str) -> Generator:
    with open(file_path, "rb") as file:
        yield file.read()


@app.get("/download-large-file/{name}")
async def download_large_file(name: str):
    gen_expr = generator_file(file_path=f"./data/{name}")
    response = StreamingResponse(content=gen_expr, status_code=200)
    return response


@app.get("/")
def read_root() -> str:
    return "Hello, world!"


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", reload=True, port=int(os.getenv("PORT", "8080")))
