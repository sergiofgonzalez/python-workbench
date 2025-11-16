"""Illustrates how to create classes that can be used as decorators."""

import functools
from collections.abc import Callable
from time import perf_counter
from typing import Any


def log_time(
    label: str | None = None,
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """Print in stdout the execution time of the function to which it is applied."""

    def log_time_decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        """Implement the log_time decorator."""

        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:  # noqa: ANN401
            start_ts = perf_counter()
            result = func(*args, **kwargs)
            duration = perf_counter() - start_ts
            if label:
                print(f">>> [{label}] {func.__name__!r} {duration:.6f} seconds")
            else:
                print(f">>> {func.__name__!r} {duration:.6f} seconds")
            return result

        return wrapper

    return log_time_decorator


@log_time("performance")
def calculate_sum_of_numbers(n: int) -> int:
    """Return the sum of the first n integers."""
    if n < 0:
        msg = "n must be positive"
        raise ValueError(msg)
    return sum(range(1, n + 1))


class TimeLogger:
    """Class that can be used to decorate functions and get execution time."""

    def __init__(self, label: str | None = None) -> None:
        """Initialize an instance of TimeLogger instances."""

        def log_time_decorator(func: Callable[..., Any]) -> Callable[..., Any]:
            """Implement the log_time decorator."""

            @functools.wraps(func)
            def wrapper(*args: Any, **kwargs: Any) -> Any:  # noqa: ANN401
                start_ts = perf_counter()
                result = func(*args, **kwargs)
                duration = perf_counter() - start_ts
                if label:
                    print(f">>> [{label}] {func.__name__!r} {duration:.6f} seconds")
                else:
                    print(f">>> {func.__name__!r} {duration:.6f} seconds")
                return result

            return wrapper

        self.log_time = log_time_decorator
        self.label = label

    def __call__(self, *args: Callable[..., Any]) -> Callable[..., Any]:
        """Make TimeLogger callable."""
        return self.log_time(*args)


@TimeLogger("performance")
def calculate_sum_of_ints(n: int) -> int:
    """Return the sum of the first n integers."""
    if n < 0:
        msg = "n must be positive"
        raise ValueError(msg)
    return sum(range(1, n + 1))


def main() -> None:
    """Application entry point."""
    print(calculate_sum_of_numbers(1))
    print(calculate_sum_of_numbers(2))
    print(calculate_sum_of_numbers(3))
    print(calculate_sum_of_numbers(1_000_000))

    # Now with the TimeLogger class
    print(calculate_sum_of_ints(1))
    print(calculate_sum_of_ints(2))
    print(calculate_sum_of_ints(3))
    print(calculate_sum_of_ints(1_000_000))


if __name__ == "__main__":
    main()
