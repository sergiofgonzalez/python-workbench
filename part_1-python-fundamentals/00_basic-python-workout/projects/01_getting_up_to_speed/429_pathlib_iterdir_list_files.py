"""Illustrates how to use pathlib.Path.iterdir() to list files in a directory."""

from pathlib import Path


def main() -> None:
    """Application entry point."""
    directory = Path()  # Current directory
    for entry in directory.iterdir():
        if entry.is_file():
            print(f"File: {entry.name}")
        else:
            print(f"Not a file: {entry.name}")


if __name__ == "__main__":
    main()
