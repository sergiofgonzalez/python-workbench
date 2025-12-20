"""A basic reimplementation of Unix's wc (word count) utility."""

import sys
from pathlib import Path


def main() -> None:
    """Application entry point."""
    if len(sys.argv) < 2:  # noqa: PLR2004
        print("Usage: python main.py <filename>")
        sys.exit(1)

    filename = sys.argv[1]
    line_count = 0
    word_count = 0
    byte_count = 0
    try:
        with Path(filename).open("r", encoding="utf-8") as file:
            for line in file:
                line_count += 1
                word_count += len(line.split())
                byte_count += len(line.encode("utf-8"))  # Count bytes in UTF-8 encoding
    except FileNotFoundError:
        print(f"{filename}: No such file")
        sys.exit(1)

    print(f"{line_count} {word_count} {byte_count} {filename}")


if __name__ == "__main__":
    main()
