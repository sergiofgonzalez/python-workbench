"""Illustrate how to create an infinite generator."""
from collections.abc import Iterator


def count() -> Iterator[int]:
    """Generate an infinite sequence of integers starting from 0."""
    n = 0
    while True:
        yield n
        n += 1

def main() -> None:
    """Application entry point."""
    # naively invoking the generator function to print the first three elements
    print(count())
    print(count())
    print(count())

    # using the generator to print the first three elements
    for num in count():
        print(num)
        if num >= 10:  # noqa: PLR2004
            break

    # alternatively, you can instantiate the generator
    infinite_counter = count()
    for num in infinite_counter:
        print(num)
        if num >= 10:  # noqa: PLR2004
            break

    # You can also use next() to get the next value from the generator
    infinite_counter = count()
    for _ in range(3):
        print(next(infinite_counter))


if __name__ == "__main__":
    main()
