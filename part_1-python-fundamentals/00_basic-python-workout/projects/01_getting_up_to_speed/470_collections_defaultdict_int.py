"""Illustrates how to use collections.defaultdict."""

from collections import defaultdict


def main() -> None:
    """Application entry point."""
    sentence = "the quick brown fox jumps over the lazy dog"

    # counting the words in a sentence using a regular dict
    word_counts: dict[str, int] = {}
    for word in sentence.split():
        if word in word_counts:
            word_counts[word] += 1
        else:
            word_counts[word] = 1
    print(f"Word counts using regular dict: {word_counts}")
    print("-" * 40)

    # counting the words in a sentence using defaultdict
    word_counts_dd = defaultdict(int)
    for word in sentence.split():
        word_counts_dd[word] += 1
    print(f"Word counts using defaultdict: {word_counts_dd}")
    print("-" * 40)


if __name__ == "__main__":
    main()
