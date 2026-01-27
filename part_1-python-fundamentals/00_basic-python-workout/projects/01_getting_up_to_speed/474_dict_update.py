"""Illustrates how to work with the dict.update() method."""


def main() -> None:
    """Application entry point."""
    numbers = {"ONE": 1, "TWO": 2, "THREE": 3}

    # Using update to create one more key-value pair
    numbers.update(FOUR=4)
    print(numbers)  # {'ONE': 1, 'TWO': 2, 'THREE': 3, 'FOUR': 4}
    assert numbers == {"ONE": 1, "TWO": 2, "THREE": 3, "FOUR": 4}
    print("-" * 40)

    # Using dict.update() to add more key-value pairs
    numbers.update({"FIVE": 5, "SIX": 6})
    print(numbers)  # {'ONE': 1, 'TWO': 2, 'THREE': 3, 'FOUR': 4, 'FIVE': 5, 'SIX': 6}
    assert numbers == {"ONE": 1, "TWO": 2, "THREE": 3, "FOUR": 4, "FIVE": 5, "SIX": 6}
    print("-" * 40)

    # using update with an existing key updates its value
    numbers.update(FOUR=14)
    print(numbers)  # {'ONE': 1, 'TWO': 2, 'THREE': 3, 'FOUR': 14, 'FIVE': 5, 'SIX': 6}
    assert numbers == {"ONE": 1, "TWO": 2, "THREE": 3, "FOUR": 14, "FIVE": 5, "SIX": 6}
    print("-" * 40)

    # you can also use update with another dict containing both existing and new keys
    more_numbers = {"FOUR": 4, "SEVEN": 7, "EIGHT": 8}
    numbers.update(more_numbers)
    print(numbers)
    assert numbers == {
        "ONE": 1,
        "TWO": 2,
        "THREE": 3,
        "FOUR": 4,
        "FIVE": 5,
        "SIX": 6,
        "SEVEN": 7,
        "EIGHT": 8,
    }
    print("-" * 40)


if __name__ == "__main__":
    main()
