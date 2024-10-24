"""A basic sync context manager using generators."""

from collections.abc import Generator
from contextlib import contextmanager
from pathlib import Path
from typing import IO


@contextmanager
def open_file(file_name: str, method: str) -> Generator[IO, None, None]:
    """Context Manager for opening a file as a context manager."""
    f = Path.open(Path(file_name), method)
    try:
        yield f
    finally:
        f.close()


def main() -> None:
    """Application entry point."""
    with open_file("my_file.txt", "w") as file:
        file.write("Hello to Jason Isaacs!")

    with open_file("my_file.txt", "r") as file:
        file.made_up_method("hello, hello!")


if __name__ == "__main__":
    main()
