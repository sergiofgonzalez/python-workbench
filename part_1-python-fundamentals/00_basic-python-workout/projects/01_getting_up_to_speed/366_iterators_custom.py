"""Illustrate custom iterators."""

from collections.abc import Iterable, Iterator


class FibonacciIterator:
    """An iterator that generates Fibonacci numbers."""

    def __init__(self, n: int) -> None:
        """Initialize the iterator with the number of elements to generate."""
        self.n = n
        self.count = 0
        self.a, self.b = 0, 1

    def __iter__(self) -> "FibonacciIterator":
        """Return the iterator object itself."""
        return self

    def __next__(self) -> int:
        """Return the next Fibonacci number."""
        if self.count < self.n:
            self.count += 1
            a, b = self.a, self.b
            self.a, self.b = b, a + b
            return a
        raise StopIteration


def main() -> None:
    """Application entry point."""
    n = 10
    fib_iterator = FibonacciIterator(n)
    for num in fib_iterator:
        print(num)

    fib_iterator = FibonacciIterator(8)
    print("First 8 Fibonacci numbers:")
    fib_nums = [next(fib_iterator) for _ in range(8)]
    print(fib_nums)

    fib_iterator = FibonacciIterator(9)
    print("First 9 Fibonacci numbers:")
    print(list(fib_iterator))

    if isinstance(fib_iterator, Iterator):
        print("fib_iterator is an instance of Iterator")

    if isinstance(fib_iterator, Iterable):
        print("fib_iterator is also an instance of Iterable")


if __name__ == "__main__":
    main()
