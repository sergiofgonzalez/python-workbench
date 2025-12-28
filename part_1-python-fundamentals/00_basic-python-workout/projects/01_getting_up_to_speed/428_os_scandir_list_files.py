"""Illustrates how to use os.scandir() to list files in a directory."""

import os


def main() -> None:
    """Application entry point."""
    directory = "."  # Current directory
    with os.scandir(directory) as entries:
        for entry in entries:
            if entry.is_file():
                print(f"File: {entry.name}")
            else:
                print(f"Not a file: {entry.name}")


if __name__ == "__main__":
    main()
