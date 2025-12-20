"""Illustrates the basics of generators."""

from collections.abc import Generator


def four() -> Generator[int]:
    """Yield the values from 0 to 4."""
    i = 0
    while i <= 4:  # noqa: PLR2004
        yield i
        i += 1


def main() -> None:
    """Application entry point."""
    for value in four():
        print(f"Value from generator: {value}")
    print("=" * 40)
    # using next()
    gen = four()
    print(f"First value from generator using next(): {next(gen)}")
    print(f"Second value from generator using next(): {next(gen)}")
    print(f"Third value from generator using next(): {next(gen)}")
    print(f"Fourth value from generator using next(): {next(gen)}")
    print(f"Fifth value from generator using next(): {next(gen)}")
    # Raises StopIteration
    try:
        print(f"Sixth value from generator using next(): {next(gen)}")
    except StopIteration as e:
        print(f"Reached the end of the generator; StopIteration raised: '{e=}'.")


if __name__ == "__main__":
    main()
