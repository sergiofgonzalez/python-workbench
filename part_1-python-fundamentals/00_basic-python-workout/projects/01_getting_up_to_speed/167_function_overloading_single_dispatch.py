"""Illustrate how to do function overloading in Python with single dispatch."""

from functools import singledispatch
from typing import Any


@singledispatch
def process_data(data: Any) -> str:  # noqa: ANN401
    """Process data based on its type."""
    return f"Received type {type(data).__name__}"


@process_data.register
def _(data: int) -> str:
    """Process integer data."""
    return f"Processing integer: {data}"


@process_data.register
def _(data: str) -> str:
    """Process string data."""
    return f"Processing string: {data}"


@process_data.register
def _(data: list) -> str:
    """Process list data."""
    return f"Processing list with {len(data)} elements: {data}"


class Person:
    """A simple class to demonstrate single dispatch with custom types."""

    def __init__(self, name: str) -> None:
        """Initialize a Person with a name."""
        self.name = name

    def __repr__(self) -> str:
        """Return a string representation of the Person."""
        return f"Person(name={self.name})"


def main() -> None:
    """Application entry point."""
    print(process_data(42))
    print(process_data("Hello"))
    print(process_data([1, 2, 3]))
    print(process_data(Person("Alice")))
    print(process_data(3.14))  # This will use the default handler


if __name__ == "__main__":
    main()
