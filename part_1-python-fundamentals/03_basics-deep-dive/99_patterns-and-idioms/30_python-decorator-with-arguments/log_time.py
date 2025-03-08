"""A Python decorator that logs a function/method exec time and accepts arguments."""

import time
from collections.abc import Callable


def log_time(label: str | None = None) -> Callable:
    """Python decorator accepting an argument label."""

    def log_time_decorator(fn: Callable) -> Callable:
        """Implement the Python decorator as per spec (accept fn, return fn)."""
        nonlocal label

        def wrapper(*args: any, **kwargs: any) -> any:
            """Report invocation time."""
            start = time.perf_counter()
            result = fn(*args, **kwargs)
            print(
                f"{label}: {time.perf_counter() - start:.3f} seconds",
                # f"{label if label else fn.__name__}: {time.perf_counter() - start:.3f} seconds"
            )
            return result

        if label is None:
            label = fn.__name__
        return wrapper

    return log_time_decorator
