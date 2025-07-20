"""Illustrate the use case for nonlocal when using nested functions."""

from collections.abc import Callable


def count() -> Callable[[], int]:
    """Return a function that counts the number of times it has been called."""
    count_value = 0

    def inner() -> int:
        nonlocal count_value  # Use nonlocal to modify the outer variable
        count_value += 1
        return count_value

    return inner


def main() -> None:
    """Application entry point."""
    counter = count()

    print("Calling counter() multiple times:")
    for _ in range(5):
        print(f"Counter value: {counter()}")  # Should print 1, 2, 3, 4, 5

if __name__ == "__main__":
    main()
