"""Illustrates the basics of FastAPI request files."""

from typing import Annotated

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse

app = FastAPI()


@app.post("/files/")
async def create_file(file: Annotated[bytes, File()]) -> dict[str, int]:
    """Path operation for the POST /files/ endpoint."""
    return {"file_length": len(file)}


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile) -> dict[str, str | None]:
    """Path operation for the POST /uploadfiles/ endpoint."""
    return {"filename": file.filename, "content_type": file.content_type}


@app.post("/v2/files/")
async def create_file_v2(
    file: Annotated[bytes | None, File()] = None,
) -> dict[str, int | str]:
    """Path operation for the POST /files/ endpoint."""
    if file is None:
        return {"message": "No file sent"}
    return {"file_length": len(file)}


@app.post("/v2/uploadfile/")
async def create_upload_file_v2(
    file: Annotated[UploadFile | None, File()] = None,
) -> dict[str, str | None]:
    """Path operation for the POST /uploadfiles/ endpoint."""
    if file is None:
        return {"message": "No upload file sent"}
    return {"filename": file.filename, "content_type": file.content_type}


@app.post("/v3/files/")
async def create_file_v3(
    file: Annotated[bytes, File(description="A file read as bytes")],
) -> dict[str, int]:
    """Path operation for the POST /files/ endpoint."""
    return {"file_length": len(file)}


@app.post("/v3/uploadfile/")
async def create_upload_file_v3(
    file: Annotated[UploadFile, File(description="A file read as UploadFile")],
) -> dict[str, str | None]:
    """Path operation for the POST /uploadfiles/ endpoint."""
    return {"filename": file.filename, "content_type": file.content_type}


@app.post("/v4/files/")
async def create_file_v4(
    files: Annotated[list[bytes], File()],
) -> list[dict[str, int]]:
    """Path operation for the POST /files/ endpoint."""
    return [{"file_length": len(file)} for file in files]


@app.post("/v4/uploadfile/")
async def create_upload_file_v4(
    files: list[UploadFile],
) -> list[dict[str, str | None]]:
    """Path operation for the POST /uploadfiles/ endpoint."""
    return [{"filename": f.filename, "content_type": f.content_type} for f in files]


@app.get("/v4")
async def read_root_v4() -> HTMLResponse:
    """Path operation for the GET /v4 endpoint."""
    return HTMLResponse(
        content="""
    <body>
      <form action="/v4/files/" enctype="multipart/form-data" method="post">
        <input name="files" type="file" multiple>
        <input type="submit" value="Send post to /v4/files/ as bytes">
      </form>
      <form action="/v4/uploadfile/" enctype="multipart/form-data" method="post">
        <input name="files" type="file" multiple>
        <input type="submit" value="Send post to /v4/uploadfile/ as UploadFile">
      </form>
    </body>
    """,
    )


@app.post("/v5/files/")
async def create_file_v5(
    files: Annotated[list[bytes], File(description="A list of files read as bytes")],
) -> list[dict[str, int]]:
    """Path operation for the POST /files/ endpoint."""
    return [{"file_length": len(file)} for file in files]


@app.post("/v5/uploadfile/")
async def create_upload_file_v5(
    files: Annotated[
        list[UploadFile],
        File(description="A list of files read as UploadFile"),
    ],
) -> list[dict[str, str | None]]:
    """Path operation for the POST /uploadfiles/ endpoint."""
    return [{"filename": f.filename, "content_type": f.content_type} for f in files]


@app.get("/v5")
async def read_root_v5() -> HTMLResponse:
    """Path operation for the GET /v5 endpoint."""
    return HTMLResponse(
        content="""
    <body>
      <form action="/v5/files/" enctype="multipart/form-data" method="post">
        <input name="files" type="file" multiple>
        <input type="submit" value="Send post to /v5/files/ as bytes">
      </form>
      <form action="/v5/uploadfile/" enctype="multipart/form-data" method="post">
        <input name="files" type="file" multiple>
        <input type="submit" value="Send post to /v5/uploadfile/ as UploadFile">
      </form>
    </body>
    """,
    )
