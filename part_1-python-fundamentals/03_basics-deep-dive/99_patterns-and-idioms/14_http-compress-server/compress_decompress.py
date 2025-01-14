"""Illustrate the compress-decompress technique for streams."""

import gzip
import io
from pathlib import Path


def gzip_chunks(filename: str):
    """Open a file and return its contents in chunks gzipped."""
    with Path(filename).open("rb") as f:
        while chunk := f.read(256):
            gzipped_chunk = gzip.compress(chunk)
            yield gzipped_chunk


def gzipped_buf(filename: str):
    """Open a file and return its contents in chunks, gzipped and in a buffer."""
    buf = io.BytesIO()
    with Path(filename).open("rb") as f:
        while chunk := f.read(256):
            gzipped_chunk = gzip.compress(chunk)
            bytes_count = buf.write(gzipped_chunk)
            print(f"{bytes_count=}")
    buf.seek(0)
    return buf

def main() -> None:
    """Application entry point."""
    # Run 1: iterating over the chunks and decompressing them
    for gzipped_chunk in gzip_chunks("SOME_FILE.md"):
        # This is what happens in the v1 example
        # chunk = gzip.decompress(gzipped_chunk[0:127])
        chunk = gzip.decompress(gzipped_chunk)
        print(chunk)

    # Run 2: I put the compressed chunks in a buffer
    buffer = gzipped_buf("SOME_FILE.md")
    while gzipped_chunk := buffer.read(256):
        chunk = gzip.decompress(gzipped_chunk)
        print(chunk)

if __name__ == "__main__":
    main()
