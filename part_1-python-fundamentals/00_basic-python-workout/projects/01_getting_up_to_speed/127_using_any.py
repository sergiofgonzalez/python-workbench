"""Using the any type annotation."""

from typing import Any


def foo(x: Any) -> str:  # noqa: ANN401
    """Return a string representation of the input."""
    return f"Input is: {x}"


def main() -> None:
    """Application entry point."""
    print(foo(42))  # Should print "Input is: 42"
    print(foo("Hello"))  # Should print "Input is: Hello"
    print(foo([1, 2, 3]))  # Should print "Input is: [1, 2, 3]"
    print(foo({"key": "value"}))  # Should print "Input is: {'key': 'value'}"


if __name__ == "__main__":
    main()
