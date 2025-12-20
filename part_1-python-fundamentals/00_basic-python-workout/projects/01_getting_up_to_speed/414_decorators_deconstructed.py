"""Deconstructs the magic that happens behind functions with decorators."""

import functools
import logging
from collections.abc import Callable

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

logger = logging.getLogger(__name__)


def trace(func: Callable) -> Callable:
    """Trace function calls."""

    @functools.wraps(func)
    def wrapper(*args: object, **kwargs: object) -> object:
        logger.debug("Calling %s with args=%s, kwargs=%s", func.__name__, args, kwargs)  # ty:ignore[unresolved-attribute]
        result = func(*args, **kwargs)
        logger.debug("%s returned %s", func.__name__, result)  # ty:ignore[unresolved-attribute]
        return result

    return wrapper


@trace
def add(a: int, b: int) -> int:
    """Return the sum of two integers."""
    return a + b


def subtract(a: int, b: int) -> int:
    """Return the difference of two integers."""
    return a - b


def main() -> None:
    """Application entry point."""
    sum_result = add(3, 5)
    print(f"Sum result: {sum_result}")
    print("=" * 40)

    # Manually applying the decorator to the subtract function
    traced_subtract = trace(subtract)
    diff_result = traced_subtract(10, 4)
    print(f"Difference result: {diff_result}")


if __name__ == "__main__":
    main()
