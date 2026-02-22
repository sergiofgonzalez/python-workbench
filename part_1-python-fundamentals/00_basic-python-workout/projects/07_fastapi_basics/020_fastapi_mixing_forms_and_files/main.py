"""Illustrates how to mix forms and files in FastAPI."""

from typing import Annotated

from fastapi import FastAPI, File, Form, UploadFile

app = FastAPI()


@app.post("/files/")
async def read_files_and_form_field(
    file_a: Annotated[bytes, File()],
    file_b: UploadFile,
    token: Annotated[str, Form()],
) -> dict[str, str | int | None]:
    """Path operation for the POST /files/ endpoint that also receives a form field."""
    return {
        "file_a_length": len(file_a),
        "file_b_filename": file_b.filename,
        "file_b_content_type": file_b.content_type,
        "token": token,
    }
