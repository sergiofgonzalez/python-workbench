"""Normalizing a text file (as a 1st step for further processing)."""

import string
from pathlib import Path

in_file_path = Path("data/moby_01.txt")
out_file_path = Path("data/moby_01_normalized.txt")


def main() -> None:
    """Application entry point."""
    translation_table = str.maketrans("", "", string.punctuation)
    with (
        in_file_path.open("r", encoding="utf-8") as in_file,
        out_file_path.open("w", encoding="utf-8") as out_file,
    ):
        for line in in_file:
            normalized_line = line.lower().strip()
            normalized_line = normalized_line.translate(translation_table)
            words = normalized_line.split()
            for word in words:
                out_file.write(f"{word}\n")


if __name__ == "__main__":
    main()
