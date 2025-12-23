"""Reporting utilities for word frequency counter project."""

from utils.counting import (
    get_top_n_least_common_words,
    get_top_n_most_common_words,
)


def print_word_count(word: str, count: int) -> None:
    """Prints the word count in a formatted manner."""
    print(f"{word!r} occurs {count} time{'s' if count != 1 else ''}.")


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
