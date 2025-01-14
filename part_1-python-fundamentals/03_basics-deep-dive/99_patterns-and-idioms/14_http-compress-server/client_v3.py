"""HTTP client that sends a file in stream mode to an HTTP server."""

import gzip
import io
from pathlib import Path
from typing import Annotated

import requests
import typer



def send_gzipped_file(filename: Annotated[
        Path,
        typer.Argument(
            exists=True,
            dir_okay=False,
            file_okay=True,
            readable=True,
            resolve_path=False,
            show_default=False,
            help="Path to the file to send to the server",
        ),
    ]) -> None:
    with filename.open("rb") as f, io.BytesIO() as buf:
        while chunk := f.read(256):
            buf.write(gzip.compress(chunk))
        buf.seek(0)
        response = requests.put(
            "http://localhost:8000",
            headers={
                "Content-Type": "application/octet-stream",
                "X-Filename": filename.name,
                "Content-Encoding": "gzip",
            },
            data=buf.getvalue(),
        )
    if response.status_code == 201:
        print("Request ended successfully")
    else:
        print(f"Could not send request: {response.status_code}: {response.text()}")


if __name__ == "__main__":
    typer.run(send_gzipped_file)
