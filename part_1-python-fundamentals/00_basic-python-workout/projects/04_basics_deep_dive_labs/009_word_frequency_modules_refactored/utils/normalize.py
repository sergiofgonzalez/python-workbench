"""Text Processing Normalization utilities for word frequency counter project."""

import string
from pathlib import Path


def normalize_text_file(in_file_path: Path, out_file_path: Path) -> None:
    """Normalize a text file and write normalized words to an output file."""
    with (
        in_file_path.open("r", encoding="utf-8") as in_file,
        out_file_path.open("w", encoding="utf-8") as out_file,
    ):
        for line in in_file:
            words = normalize_text_line(line)
            for word in words:
                out_file.write(f"{word}\n")


def normalize_text_line(line: str) -> list[str]:
    """Normalize a textline.

    Normalize a line of text by lowercasing, stripping punctuation, and splitting into
    words.

    Args:
       line (str): A line of text to normalize.

    Returns:
       list[str]: A list of normalized words.
    """
    translation_table = str.maketrans("", "", string.punctuation)
    normalized_line = line.lower().strip()
    normalized_line = normalized_line.translate(translation_table)
    return normalized_line.split()
