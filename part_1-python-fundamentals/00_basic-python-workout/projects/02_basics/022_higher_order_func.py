"""Illustrate higher-order functions in Python."""

from collections.abc import Callable


def add(x: float, y: float) -> float:
    """Return the sum of x and y."""
    return x + y


def sub(x: float, y: float) -> float:
    """Return the difference of x and y."""
    return x - y


def compute(x: float, y: float, op: Callable[[float, float], float]) -> float:
    """Return the result of applying the operation op to x and y."""
    return op(x, y)


def main() -> None:
    """Application entry point."""
    assert add(2.0, 3.0) == 5.0, "Expected 5.0"  # noqa: PLR2004
    assert sub(2.0, 3.0) == -1.0, "Expected -1.0"
    assert compute(2.0, 3.0, add) == 5.0, "Expected 5.0"  # noqa: PLR2004
    assert compute(2.0, 3.0, sub) == -1.0, "Expected -1.0"


if __name__ == "__main__":
    main()
