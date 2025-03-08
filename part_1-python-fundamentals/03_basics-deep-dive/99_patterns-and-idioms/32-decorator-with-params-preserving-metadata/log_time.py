"""A decorator accepting parameter that uses functools.wraps to preserve the docs."""

import functools
import time


def log_time(label: str | None = None) -> callable:
    """Log time and prints a custom label."""

    def log_time_decorator(fn: callable) -> callable:
        @functools.wraps(fn)
        def wrapper(*args: any, **kwargs: any) -> any:
            start = time.perf_counter()
            result = fn(*args, **kwargs)
            print(
                f"{label if label else fn.__name__}: ",
                f"{time.perf_counter() - start:.3f} seconds",
            )
            return result

        return wrapper

    return log_time_decorator
