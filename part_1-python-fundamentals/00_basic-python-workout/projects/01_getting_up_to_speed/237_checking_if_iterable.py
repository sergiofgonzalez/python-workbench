"""Checking if an object is iterable using EAFP approach."""

from typing import Any


def is_iterable(obj: Any) -> bool:  # noqa: ANN401
    """Check if an object is iterable."""
    try:
        _ = iter(obj)
    except TypeError as err:
        print(f"object passed of type {type(obj).__name__} is not iterable: {err}")
        return False
    else:
        print(f"object passed of type {type(obj).__name__} is iterable")
        return True


def main() -> None:
    """Application entry point."""
    is_iterable(5)
    is_iterable([1, 2, 3])
    is_iterable("Hello")
    is_iterable((1, 2, "Hello"))
    is_iterable({1: "one", 2: "two"})


if __name__ == "__main__":
    main()
