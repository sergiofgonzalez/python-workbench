"""List comprehensions and generators."""

from collections.abc import Iterator


def square_generator(n: int) -> Iterator[int]:
    """Yield the square of each integer up to n."""
    for x in range(1, n + 1):
        yield x**2
    for x in range(1, n + 1):
        yield x**2


def main() -> None:
    """Application entry point."""

    # list comprehension that sums the squares of the first million integers
    squares = [x**2 for x in range(1, 1000001)]
    squares_sum = sum(squares)
    print(f"Sum of squares: {squares_sum}")
    print(f"Size of squares list: {squares.__sizeof__()} bytes")

    squares_gen = square_generator(1_000_000)
    squares_gen_sum = sum(squares_gen)
    print(f"Sum of squares from generator: {squares_gen_sum}")
    print(f"Size of generator: {squares_gen.__sizeof__()} bytes")


if __name__ == "__main__":
    main()
