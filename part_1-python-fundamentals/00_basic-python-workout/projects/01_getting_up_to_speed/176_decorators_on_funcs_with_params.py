"""Illustrate how to create decorators for functions that receive params."""

from collections.abc import Callable
from typing import Any


def announce(func: Callable[..., Any]) -> Callable[..., Any]:
    """Announce function calls."""

    def wrapper(*args: Any, **kwargs: Any) -> Any:  # noqa: ANN401
        """Add announcement to function call."""
        print(
            f">>> About to call the function {func.__name__} "
            f"with args: {args} and kwargs: {kwargs}",
        )
        result = func(*args, **kwargs)
        print(f">>> Function call to {func.__name__} completed.")
        return result

    return wrapper


@announce
def say_hello() -> None:
    """Say hello."""
    print("Hello, world!")


@announce
def greet(name: str) -> None:
    """Greet a person by name."""
    print(f"Hello, {name}!")


@announce
def get_greeting(name: str, age: int) -> str:
    """Return a greeting message."""
    return f"Hello, {name}! You are {age} years old."


def main() -> None:
    """Application entry point."""
    say_hello()
    greet("Alice")
    greeting = get_greeting("Bob", 30)
    print(greeting)


if __name__ == "__main__":
    main()
