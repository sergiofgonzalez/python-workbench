"""Illustrate how functions are first class citizens in Python."""

from collections.abc import Callable


def get_mean(data: list[float]) -> str:  # noqa: ARG001
    """Return self-announce."""
    return "get_mean called"


def get_min(data: list[float]) -> str:  # noqa: ARG001
    """Return self-announce."""
    return "get_min called"


def get_max(data: list[float]) -> str:  # noqa: ARG001
    """Return self-announce."""
    return "get_max called"


def process_data(data: list[float], fn: Callable[[list[float]], str]) -> str:
    """Process data using the provided function."""
    return fn(data)


def main() -> None:
    """Application entry point."""
    fns = {
        "mean": get_mean,
        "min": get_min,
        "max": get_max,
    }
    data = [1.0, 2.0, 3.0, 4.0, 5.0]
    for name, fn in fns.items():
        result = process_data(data, fn)
        print(f"{name}: {result}")


if __name__ == "__main__":
    main()
