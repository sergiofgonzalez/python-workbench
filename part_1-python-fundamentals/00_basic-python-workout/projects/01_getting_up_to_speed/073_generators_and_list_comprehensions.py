"""Illustrate how to collect generator values in a list comprehensions."""

from collections.abc import Iterator


def count(start: int, end: int) -> Iterator[int]:
    """Generate a sequence of integers from start to end (inclusive)."""
    for n in range(start, end + 1):  # noqa: UP028
        yield n


def main() -> None:
    """Application entry point."""
    # Collecting the values from the generator in a list using a list comprehension
    numbers = [n for n in count(1, 10)]  # noqa: C416
    print(f"Numbers from 1 to 10: {numbers}")

    # There's a cleaner syntax using list() directly on the generator
    numbers = list(count(1, 10))
    print(f"Numbers from 1 to 10: {numbers}")


if __name__ == "__main__":
    main()
