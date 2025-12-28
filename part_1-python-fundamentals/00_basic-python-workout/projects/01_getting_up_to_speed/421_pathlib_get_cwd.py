"""Illustrates how to get the current working directory using pathlib."""

from pathlib import Path


def main() -> None:
    """Application entry point."""
    print(f"{Path()=}")  # Current directory as Path object '.' (relative)
    print(f"{Path.cwd()=}")  # Current directory as absolute Path object


if __name__ == "__main__":
    main()
