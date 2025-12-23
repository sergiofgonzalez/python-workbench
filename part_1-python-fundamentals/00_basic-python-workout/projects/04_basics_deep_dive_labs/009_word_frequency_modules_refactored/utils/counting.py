"""Counting utilities for word frequency counter project."""

from pathlib import Path


def get_word_count(in_normalized_file_path: Path) -> dict[str, int]:
    """Get word count from a text file that has been already normalized."""
    word_count: dict[str, int] = {}
    with in_normalized_file_path.open("r", encoding="utf-8") as in_file:
        for word in in_file:
            stripped_word = word.strip()
            word_count[stripped_word] = word_count.get(stripped_word, 0) + 1
    return word_count


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
