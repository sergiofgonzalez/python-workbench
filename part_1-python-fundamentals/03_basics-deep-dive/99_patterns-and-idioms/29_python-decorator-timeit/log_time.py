"""A Python decorator that logs in the terminal how long a function took to complete."""

import time


def log_time(fn: callable) -> callable:
    """Print in the terminal how long it took to execute the function."""

    def time_fn_exec(*args: any, **kwargs: any) -> any:
        print(f"--- {fn.__name__} execution started")
        start_ts = time.perf_counter()
        result = fn(*args, **kwargs)
        print(
            f"*** {fn.__name__} "
            f"execution took {time.perf_counter() - start_ts:.3f} sec",
        )
        return result

    return time_fn_exec
