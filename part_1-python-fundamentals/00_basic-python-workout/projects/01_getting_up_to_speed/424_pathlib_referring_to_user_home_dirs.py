"""Illustrates how to refer to user and home directories with pathlib."""

from pathlib import Path


def main() -> None:
    """Application entry point."""
    print(f"{Path.home()=}")  # User's home directory
    print(f"{Path("~").expanduser()=}")  # User's home directory using expanduser

    # The second one is especially useful when dealing with paths
    print(f"{Path('~/Downloads/videos/movie.mp4').expanduser()=}")


if __name__ == "__main__":
    main()
