"""Illustrate how create a @monitor decorator to track function calls."""

from collections.abc import Callable
from random import uniform
from time import sleep
from typing import Any


def monitor(func: Callable[..., Any]) -> Callable[..., Any]:
    """Monitor function calls with arguments and return values."""

    def wrapper(*args: Any, **kwargs: Any) -> Any:  # noqa: ANN401
        """Wrap the function to monitor its execution."""
        print(
            f">>> {func.__name__!r} invoked: {args=};{kwargs=}.",
        )
        result = func(*args, **kwargs)
        print(f">>> {func.__name__!r} returned {result!r}.")
        return result

    return wrapper


@monitor
def run_with_random_delay() -> float:
    """Run a function with a delay."""
    delay = uniform(1, 5)  # Random delay between 1 and 5 seconds  # noqa: S311
    sleep(delay)
    return delay


@monitor
def run_with_delay(
    min_wait: float,
    max_wait: float,
    *,
    label: str | None = None,
    verbose: bool = False,
) -> float:
    """Run a function with a delay."""
    if label:
        print(f"{label}: about to execute")
    delay = uniform(min_wait, max_wait)  # noqa: S311
    if verbose:
        print(f"Delaying for {delay:.2f} seconds")
    sleep(delay)
    if verbose:
        print(f"Delaying for {delay:.2f} seconds completed")
    if label:
        print(f"{label}: completed")
    return delay


def main() -> None:
    """Application entry point."""
    delay = run_with_random_delay()
    print(f"Function completed with a delay of {delay:.2f} seconds.")
    print("===" * 10)
    delay = run_with_delay(1, 5, label="Test Function", verbose=True)
    print(f"Function completed with a delay of {delay:.2f} seconds.")


if __name__ == "__main__":
    main()
