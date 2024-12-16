"""Illustration the continuation-passing style and the callback pattern."""

from collections.abc import Callable


def add(a: float, b: float, cb: Callable[[float], None]) -> None:
    """Illustrate the CPS style to propagate the sum of the numbers given."""
    cb(a + b)


def print_result_by_2(value: float) -> None:
    """Print the result of the operation, after having multiplied it by 2."""
    print(f"Result times two is {value * 2}.")


def main() -> None:
    """Application entry point."""
    # passing a cb that doesn't return anything
    add(2, 3, lambda result: print(f"The result of the sum is {result}."))

    add(2, 3, print_result_by_2)

if __name__ == "__main__":
    main()
