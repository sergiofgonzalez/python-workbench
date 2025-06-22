"""Illustrate the use of anonymous inline functions aka Lambdas in Python."""

from collections.abc import Callable


def compute(
    x: float, y: float, z: float, op: Callable[[float, float, float], float]
) -> float:
    """Compute the result of applying a binary operation on x and y."""
    return op(x, y, z)


def main() -> None:
    """Application entry point."""
    add_three = lambda x, y, z: x + y + z  # noqa: E731
    print(compute(1, 2, 3, add_three))


if __name__ == "__main__":
    main()
