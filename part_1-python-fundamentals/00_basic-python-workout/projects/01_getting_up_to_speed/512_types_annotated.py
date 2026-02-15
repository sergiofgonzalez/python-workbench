"""Illustrates how to use `typing.Annotated`."""

from typing import Annotated


def say_hello(name: Annotated[str, "The name of the person to greet"]) -> str:
    """Return a greeting."""
    return f"Hello, {name}!"


def main() -> None:
    """Application entry point."""
    greeting = say_hello(name="Alice")
    print(greeting)


if __name__ == "__main__":
    main()
