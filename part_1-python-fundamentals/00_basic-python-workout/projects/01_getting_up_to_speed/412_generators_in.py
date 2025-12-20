"""Illustrates the use of the 'in' keyword with generators."""

from collections.abc import Generator


def four() -> Generator[int]:
    """Yield the values from 0 to 4."""
    i = 0
    while i <= 4:  # noqa: PLR2004
        yield i
        i += 1


def main() -> None:
    """Application entry point."""
    assert 2 in four()  # noqa: PLR2004
    assert 5 not in four()  # noqa: PLR2004
    print("=== All assertions passed! ===")

    print("Values in generator:", list(four()))


if __name__ == "__main__":
    main()
