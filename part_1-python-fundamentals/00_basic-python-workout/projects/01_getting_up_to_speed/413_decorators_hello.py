"""TODO: description of the program."""

import functools
from collections.abc import Callable


def html_wrapper(func: Callable[[], str]) -> Callable[[], str]:
    """Wrap the output of a function in HTML tags."""

    @functools.wraps(func)
    def wrapper(*args: object, **kwargs: object) -> str:
        return f"<html>{func(*args, **kwargs)}</html>"

    return wrapper


@html_wrapper
def hello(n: str | None = None) -> str:
    """Return a simple hello message."""
    if n:
        return f"Hello to {n}!"
    return "Hello, World!"


def main() -> None:
    """Application entry point."""
    print(hello())
    print(hello("Alice"))  # ty:ignore[too-many-positional-arguments]


if __name__ == "__main__":
    main()
