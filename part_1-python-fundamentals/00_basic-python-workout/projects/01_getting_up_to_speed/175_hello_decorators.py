"""Illustrate the basics of decorators in Python."""

from collections.abc import Callable


def announce(func: Callable[[], None]) -> Callable[[], None]:
    """Announce function calls."""

    def wrapper() -> None:
        """Add announcement to function call."""
        print(f">>> About to call the function {func.__name__}")
        result = func()
        print(f">>> Function call to {func.__name__} completed.")
        return result

    return wrapper


@announce
def say_hello() -> None:
    """Say hello."""
    print("Hello!")


# The decorator can't be applied to functions with parameters directly.
# @announce
# def greet(name: str) -> None:
#     """Greet a person by name."""
#     print(f"Hello, {name}!")  # noqa: ERA001


def main() -> None:
    """Application entry point."""
    say_hello()
    # greet("Alice")  # noqa: ERA001


if __name__ == "__main__":
    main()
