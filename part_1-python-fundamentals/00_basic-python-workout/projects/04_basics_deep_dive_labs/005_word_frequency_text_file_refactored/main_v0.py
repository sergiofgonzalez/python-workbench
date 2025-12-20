"""Calculates word frequency from a text file."""

import string
from pathlib import Path

in_file_path = Path("data/moby_01.txt")
out_file_path = Path("data/moby_01_normalized.txt")


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


def print_full_report(word_count: dict[str, int]) -> None:
    """Prints a full report of word counts."""
    for word, count in word_count.items():
        print(f"{word!r} occurs {count} time{'s' if count != 1 else ''}.")


def print_summary_report(word_count: dict[str, int]) -> None:
    """Prints a summary report of word counts."""
    print("\nSummary Report")
    print("---------------")
    sorted_word_counts = sorted(
        word_count.items(),
        key=lambda item: item[1],
    )

    print("Most common words:")
    # Get last five items in reverse order
    for word, count in sorted_word_counts[:-6:-1]:
        print(f"{word!r} occurs {count} time{'s' if count != 1 else ''}.")

    print("\nLeast common words:")
    for word, count in sorted_word_counts[:5]:
        print(f"{word!r} occurs {count} time{'s' if count != 1 else ''}.")


def main() -> None:
    """Application entry point."""
    word_count: dict[str, int] = {}
    with (
        in_file_path.open("r", encoding="utf-8") as in_file,
        out_file_path.open("w", encoding="utf-8") as out_file,
    ):
        for line in in_file:
            words = normalize_text_line(line)
            for word in words:
                out_file.write(f"{word}\n")
                word_count[word] = word_count.get(word, 0) + 1

    # Analysis complete
    print_full_report(word_count)
    print_summary_report(word_count)


if __name__ == "__main__":
    main()
