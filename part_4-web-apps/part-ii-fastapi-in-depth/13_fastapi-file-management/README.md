# FastAPI: File management considerations
> upload, download, and serving static files

## Intro

Web apps will typically need to handle file transfers in both directions. Large files may need to be transferred in chunks, so that the server doesn't run out of memory for large files.

Additionally, many web servers will need to serve static files from a given directory containing HTML, CSS, JavaScript, image files, etc.

## Uploading files

FastAPI offers two techniques for file uploads `File()` and `UploadFile`:

+ `File()` is used for a direct file upload and it is appropriate for relatively small files.
+ `UploadFile` used for uploading large files.

### `File()`

`File()` is used as the type for a direct file upload. The function in which you define such type may be defined as synchronous or asynchronous, but it is recommended to use the async version as it won't tie up your web server while the file is being uploaded.

When using this method FastAPI will receive the file in chunks and reassemble it in memory, and therefore, it is appropriate for small files.

| NOTE: |
| :---- |
| This approach requires the `python-multipart` and `aiofiles` packages to be installed. |

```python
@app.post("/upload-small-file")
async def upload_small_file(uploaded_file: bytes = File()) -> str:
    return f"File size: {len(uploaded_file)} bytes"
```

### `UploadFile`

For large files, `UploadFile`is the recommended approach, as it recreates the uploaded file without requiring a large memory block.

```python
@app.post("/upload-large-file")
async def upload_large_file(uploaded_file: UploadFile) -> str:
    return (
        f"File size: {uploaded_file.size} bytes, name: {uploaded_file.filename}"
    )
```

## Downloading Files

Similarly to uploading files, there are two available techniques to download files in FastAPI:

+ `FileResponse()` is used for a direct file download and it is appropriate for relatively small files.
+ `StreamingResponse` is used to return files in chunks.

### Using `FileResponse`

`FileResponse` is an appropriate technique for small files. When using this technique the file is downloaded in one shot.

```python
@app.get("/download-small-file/{name}")
async def download_small_file(name: str) -> FileResponse:
    return FileResponse(f"./data/{name}")
```

### Using StreamingResponse

For downloading large files FastAPI provides `StreamingResponse` which returns the file in chunks.

```python
def generator_file(file_path: str) -> Generator:
    with open(file_path, "rb") as file:
        yield file.read()


@app.get("/download-large-file/{name}")
async def download_large_file(name: str):
    gen_expr = generator_file(file_path=f"./data/{name}")
    response = StreamingResponse(content=gen_expr, status_code=200)
    return response
```

## Serving Static Files

FastAPI supports serving static files as regular web servers do with `StaticFiles` object.
