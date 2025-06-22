"""Illustrate how to use the higher-order functions map, filter, reduce in Python."""

from functools import reduce


def main() -> None:
    """Application entry point."""
    numbers = [1, 2, 3, 4, 5]

    # Using map to square each number
    squared_numbers = list(map(lambda x: x**2, numbers))  # noqa: C417
    print("Squared Numbers:", squared_numbers)
    assert squared_numbers == [1, 4, 9, 16, 25]

    # Using filter to get even numbers
    even_numbers = list(filter(lambda x: x % 2 == 0, numbers))
    print("Even Numbers:", even_numbers)
    assert even_numbers == [2, 4]

    # Using reduce to sum all numbers
    total_sum = reduce(lambda x, y: x + y, numbers)
    print("Total Sum:", total_sum)
    assert total_sum == 15  # noqa: PLR2004


if __name__ == "__main__":
    main()
