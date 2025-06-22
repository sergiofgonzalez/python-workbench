"""Illustrate the use of Optional type (legacy)."""

from typing import Optional


def foo(bar: Optional[bool]) -> str:  # noqa: UP007
    """Return a string based on the input."""
    if bar is None:
        return "No value provided"
    return f"Value provided: {bar}"


def main() -> None:
    """Application entry point."""
    print(foo(None))  # Should print "No value provided"
    print(foo(True))  # Should print "Value provided: True"  # noqa: FBT003
    print(foo(False))  # Should print "Value provided: False"  # noqa: FBT003


if __name__ == "__main__":
    main()
