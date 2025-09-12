"""Decorator with parameters that also preserves metadata on the decorated function."""

import functools
from collections.abc import Callable
from random import uniform
from time import perf_counter, sleep
from typing import Any


def logtime(
    label: str | None = None,
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """Report the execution time of the function."""

    def logtime_decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        """Implement logtime decorator."""

        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:  # noqa: ANN401
            start_ts = perf_counter()
            result = func(*args, **kwargs)
            duration = perf_counter() - start_ts
            if label:
                print(f">>> [{label}] {func.__name__!r} {duration:.6f}s")
            else:
                print(f">>> {func.__name__!r} {duration:.6f}s")
            return result

        return wrapper

    return logtime_decorator


@logtime("quick function")
def say_hello() -> None:
    """Says hello."""
    print("Hello, world!")


def say_hello_with_random_delay() -> None:
    """Say hello with a random delay."""
    delay = uniform(0.5, 1.5)  # noqa: S311
    sleep(delay)
    print(f"Hello, world! (after {delay:.2f}s delay)")


def main() -> None:
    """Application entry point."""
    say_hello()
    say_hello_with_random_delay()


if __name__ == "__main__":
    main()
