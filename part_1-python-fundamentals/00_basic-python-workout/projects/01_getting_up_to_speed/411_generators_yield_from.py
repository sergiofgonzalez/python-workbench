"""Illustrates the use of the 'yield from' statement in generators."""

from collections.abc import Generator


def sub_generator(n: int) -> Generator[int]:
    """Return a list of integers from 0 to n (inc)."""
    i = 0
    while i <= n:
        yield i
        i += 1


def generator() -> Generator[int]:
    """Yield values from two sub-generators."""
    yield from sub_generator(1)
    yield from sub_generator(2)
    yield from sub_generator(3)
    yield from sub_generator(5)


def main() -> None:
    """Application entry point."""
    for value in generator():
        print(f"Value from generator: {value}")


if __name__ == "__main__":
    main()
