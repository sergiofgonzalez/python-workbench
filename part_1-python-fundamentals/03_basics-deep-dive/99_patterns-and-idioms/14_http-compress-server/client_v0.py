"""HTTP client that sends a file in stream mode to an HTTP server."""

import gzip
import io
from pathlib import Path

import requests


def gzipped_stream(filename):
    with Path(filename).open("rb") as f:
        while chunk := f.read(256):
            print("yielding chunk")
            yield gzip.compress(chunk)


def main(filename) -> None:
    for chunk in gzipped_stream("SOME_FILE.md"):
        print(chunk)
        print(gzip.decompress(chunk))


if __name__ == "__main__":
    main("README.md")
