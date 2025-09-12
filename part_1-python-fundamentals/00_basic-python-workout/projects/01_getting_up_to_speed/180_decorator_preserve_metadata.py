"""Illustrate how to use functools.wraps to preserve metadata on decorated funcs."""

import functools
from collections.abc import Callable
from typing import Any


def monitor_naive(func: Callable[..., Any]) -> Callable[..., Any]:
    """Announce function execution for tracing purposes but loses metadata on the decorated function."""  # noqa: E501

    def wrapper(*args: Any, **kwargs: Any) -> Any:  # noqa: ANN401
        print(f">>> {func.__name__!r} invoked: {args=};{kwargs=}.")
        result = func(*args, **kwargs)
        print(f">>> {func.__name__!r} returned {result!r}.")
        return result

    return wrapper


def monitor_good(func: Callable[..., Any]) -> Callable[..., Any]:
    """Announce function execution for tracing purposes preserving metadata on the decorated function."""  # noqa: E501

    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:  # noqa: ANN401
        print(f">>> {func.__name__!r} invoked: {args=};{kwargs=}.")
        result = func(*args, **kwargs)
        print(f">>> {func.__name__!r} returned {result!r}.")
        return result

    return wrapper


def say_hi() -> None:
    """Say hi function implementation."""
    print("Hi there!")


@monitor_naive
def say_hello() -> None:
    """Say hello function implementation."""
    print("Hello, there!")


@monitor_good
def say_howdy() -> None:
    """Say howdy function implementation."""
    print("Howdy!")


def main() -> None:
    """Application entry point."""
    print(f"{say_hi.__doc__=!r}; {say_hi.__name__=!r}")
    print(f"{say_hello.__doc__=!r}; {say_hello.__name__=!r}")
    print(f"{say_howdy.__doc__=!r}; {say_howdy.__name__=!r}")


if __name__ == "__main__":
    main()
