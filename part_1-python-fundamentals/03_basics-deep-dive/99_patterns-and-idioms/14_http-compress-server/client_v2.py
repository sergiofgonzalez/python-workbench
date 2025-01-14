"""HTTP client that sends a file in stream mode to an HTTP server."""

import gzip
from pathlib import Path

import requests


def main(filename) -> None:
    with Path(filename).open("rb") as f:
        response = requests.put(
            "http://localhost:8000",
            headers={
                "Content-Type": "application/octet-stream",
                "X-Filename": filename,
                "Content-Encoding": "gzip",
            },
            data=f,
            timeout=10,
        )
    if response.status_code == 201:
        print("Request ended successfully")
    else:
        print(f"Could not send request: {response.status_code}: {response.text()}")


if __name__ == "__main__":
    main("README.md")
