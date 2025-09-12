"""Illustrate how to create a decorator that logs the execution time of a function."""

from collections.abc import Callable
from random import uniform
from time import perf_counter, sleep
from typing import Any


def logtime(func: Callable[..., Any]) -> Callable[..., Any]:
    """Log the execution time of a function."""

    def wrapper(*args: Any, **kwargs: Any) -> Any:  # noqa: ANN401
        """Wrap the function to log its execution time."""
        start_time = perf_counter()
        result = func(*args, **kwargs)
        elapsed_time = perf_counter() - start_time
        print(f">>> Function {func.__name__!r} executed in {elapsed_time:.6f} seconds.")
        return result

    return wrapper


@logtime
def run_with_random_delay() -> float:
    """Run a function with a delay."""
    delay = uniform(1, 5)  # Random delay between 1 and 5 seconds  # noqa: S311
    sleep(delay)
    return delay


@logtime
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
