"""Calculates word frequency from a text file."""

import string
from pathlib import Path

in_file_path = Path("data/moby_01.txt")
out_file_path = Path("data/moby_01_normalized.txt")


def main() -> None:
    """Application entry point."""
    word_count: dict[str, int] = {}
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
                word_count[word] = word_count.get(word, 0) + 1

    # Analysis complete
    # Print full report first
    for word, count in word_count.items():
        print(f"{word!r} occurs {count} time{'s' if count != 1 else ''}.")

    # Now print the summary report with the five most common and least common words
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


if __name__ == "__main__":
    main()
