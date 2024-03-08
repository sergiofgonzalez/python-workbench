"""
Entry point for the web application
"""

import os

from fastapi import FastAPI, File, UploadFile

app = FastAPI()


@app.post("/upload-small-file")
async def upload_small_file(uploaded_file: bytes = File()) -> str:
    return f"File size: {len(uploaded_file)} bytes"


@app.post("/upload-large-file")
async def upload_large_file(uploaded_file: UploadFile) -> str:
    return (
        f"File size: {uploaded_file.size} bytes, name: {uploaded_file.filename}"
    )


@app.get("/")
def read_root() -> str:
    return "Hello, world!"


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", reload=True, port=int(os.getenv("PORT", "8080")))
