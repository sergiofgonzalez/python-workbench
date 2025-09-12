"""Illustrate how to use @cache for memoization."""

from functools import cache
from time import perf_counter


def fib(n: int) -> int:
    """Compute the nth Fibonacci number."""
    if n < 2:  # noqa: PLR2004
        return n
    return fib(n - 1) + fib(n - 2)


@cache
def cached_fib(n: int) -> int:
    """Compute the nth Fibonacci number with memoization."""
    if n < 2:  # noqa: PLR2004
        return n
    return cached_fib(n - 1) + cached_fib(n - 2)


def main() -> None:
    """Application entry point."""
    print("Calculating Fibonacci 40th number without memoization (may take a while)...")
    start_time = perf_counter()
    print(f"{fib(40)=}")
    end_time = perf_counter()
    print(f"Time taken: {end_time - start_time:.2f} seconds")

    print("Calculating Fibonacci 40th number with memoization...")
    start_time = perf_counter()
    print(f"{cached_fib(40)=}")
    end_time = perf_counter()
    print(f"Time taken: {end_time - start_time:.6f} seconds")


if __name__ == "__main__":
    main()
