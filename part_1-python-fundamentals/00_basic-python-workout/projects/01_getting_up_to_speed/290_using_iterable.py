"""Using Iterable for type checking."""

from collections.abc import Iterable
from typing import Any


def is_iterable(obj: Any) -> bool:  # noqa: ANN401
    """Return true if the received argument is iterable."""
    return isinstance(obj, Iterable)


def main() -> None:
    """Application entry point."""
    # assertions first
    assert not is_iterable(5)
    assert is_iterable([1, 2, 3])
    assert is_iterable("Hello")
    assert is_iterable((1, 2, "Hello"))
    assert is_iterable({1: "one", 2: "two"})
    assert is_iterable({1, 2, 3})

    # now we print the results
    print(f"{is_iterable(5)=}")
    print(f"{is_iterable([1, 2, 3])=}")
    print(f"{is_iterable('Hello')=}")
    print(f"{is_iterable((1, 2, 'Hello'))=}")
    print(f"{is_iterable({1: 'one', 2: 'two'})=}")
    print(f"{is_iterable({1, 2, 3})=}")


if __name__ == "__main__":
    main()
