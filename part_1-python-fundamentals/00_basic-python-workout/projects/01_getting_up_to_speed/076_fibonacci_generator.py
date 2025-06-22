"""Illustrate a generator that returns the Fibonacci sequence."""

from collections.abc import Iterator


def fibonacci() -> Iterator[int]:
    """Generate an infinite sequence of Fibonacci numbers."""
    a, b = 1, 2
    while True:
        yield a
        a, b = b, a + b


def main() -> None:
    """Application entry point."""
    print("Hello from 04-ranges-comprehensions-generators-zip!")
    for i, fib in enumerate(fibonacci()):
        print(f"Fibonacci number {i}: {fib}")
        if i >= 10:  # noqa: PLR2004
            break


if __name__ == "__main__":
    main()
