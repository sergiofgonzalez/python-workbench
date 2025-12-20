"""Calculates word frequency from a text file."""

import string
from pathlib import Path

in_file_path = Path("data/moby_01.txt")
out_file_path = Path("data/moby_01_normalized.txt")


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


def get_word_count(in_normalized_file_path: Path) -> dict[str, int]:
    """Get word count from a text file that has been already normalized."""
    word_count: dict[str, int] = {}
    with in_normalized_file_path.open("r", encoding="utf-8") as in_file:
        for word in in_file:
            stripped_word = word.strip()
            word_count[stripped_word] = word_count.get(stripped_word, 0) + 1
    return word_count


def print_full_report(word_count: dict[str, int]) -> None:
    """Prints a full report of word counts."""
    for word, count in word_count.items():
        print(f"{word!r} occurs {count} time{'s' if count != 1 else ''}.")


def print_summary_report(word_count: dict[str, int], num_words: int = 5) -> None:
    """Prints a summary report of word counts."""
    print("\n=== Summary Report ===")
    most_common_words = get_top_n_most_common_words(word_count, num_words)
    least_common_words = get_top_n_least_common_words(word_count, num_words)
    print("\nMost common words:")
    for word, count in most_common_words:
        print_word_count(word, count)
    print("\nLeast common words:")
    for word, count in least_common_words:
        print_word_count(word, count)


def get_top_n_most_common_words(
    word_count: dict[str, int],
    n: int,
) -> list[tuple[str, int]]:
    """Get the top N most common words from the word count dictionary."""
    sorted_word_counts = sorted(
        word_count.items(),
        key=lambda item: item[1],
        reverse=True,
    )
    return sorted_word_counts[:n]


def get_top_n_least_common_words(
    word_count: dict[str, int],
    n: int,
) -> list[tuple[str, int]]:
    """Get the top N least common words from the word count dictionary."""
    sorted_word_counts = sorted(
        word_count.items(),
        key=lambda item: item[1],
    )
    return sorted_word_counts[:n]


def print_word_count(word: str, count: int) -> None:
    """Prints the word count in a formatted manner."""
    print(f"{word!r} occurs {count} time{'s' if count != 1 else ''}.")


def main() -> None:
    """Application entry point."""
    normalize_text_file(in_file_path, out_file_path)
    word_count = get_word_count(out_file_path)
    print_full_report(word_count)
    print_summary_report(word_count)


if __name__ == "__main__":
    main()
