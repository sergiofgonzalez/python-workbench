"""HTTP client that sends a file in stream mode to an HTTP server."""

import gzip
from pathlib import Path

import requests


def gzipped_stream(filename):
    with Path(filename).open("rb") as f:
        while chunk := f.read(256):
            yield gzip.compress(chunk)


def main(filename) -> None:
    response = requests.put(
        "http://localhost:8000",
        headers={
            "Content-Type": "application/octet-stream",
            "X-Filename": filename,
            "Content-Encoding": "gzip",
        },
        data=gzipped_stream(filename),
        timeout=10,
    )
    if response.status_code == 201:
        print("Request ended successfully")
    else:
        print(f"Could not send request: {response.status_code}: {response.text()}")


if __name__ == "__main__":
    main("README.md")
