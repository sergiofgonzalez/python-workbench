"""Illustrates how to create a generator function that yields Fibonacci numbers."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Generator


def fib_generator(n: int) -> Generator[int]:
    """Generate Fibonacci numbers up to n."""
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b


def main() -> None:
    """Application entry point."""
    n = 10
    print(f"Fibonacci numbers up to {n}:")
    for index, fib_number in enumerate(fib_generator(n)):
        print(f"fibonacci({index}) = {fib_number}")
    print("-" * 40)

    # You can also consume it using next()
    print("\nUsing next() to get Fibonacci numbers:")
    fib_gen = fib_generator(n)
    for index in range(n):
        print(f"fibonacci({index}) = {next(fib_gen)}")


if __name__ == "__main__":
    main()
