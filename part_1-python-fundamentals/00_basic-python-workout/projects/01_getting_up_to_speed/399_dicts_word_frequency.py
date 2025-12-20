"""Compute the frequency of words in a string."""


def main() -> None:
    """Application entry point."""
    sample = "To be or not to be"

    frequency: dict[str, int] = {}
    for word in sample.split():
        word_lower = word.lower()
        if word_lower not in frequency:
            frequency[word_lower] = 0
        frequency[word_lower] += 1

    print(frequency)

    # calculate max length of words for formatting
    max_length = max(len(word) for word in frequency)

    for word, count in frequency.items():
        print(f"{word:<{max_length}} occurs {count} time{'s' if count != 1 else ''}.")



if __name__ == "__main__":
    main()
