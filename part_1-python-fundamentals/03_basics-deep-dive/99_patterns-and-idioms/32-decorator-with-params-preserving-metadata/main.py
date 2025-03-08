"""Application main program."""

import time
from random import uniform

from log_time import log_time


@log_time("custom_label")
def my_fn(sleep_sec: float | None = None) -> float:
    """Sleep for a while and return."""
    if not sleep_sec:
        sleep_sec = uniform(0.5, 1.5)  # noqa: S311
    time.sleep(sleep_sec)
    return sleep_sec


def main() -> None:
    """Application entry point."""
    print(f"Running a decorated {my_fn.__doc__}")
    result = my_fn(2.5)
    print(f"Slept for {result:.3f} seconds")
    result = my_fn()
    print(f"Slept for {result:.3f} seconds")


if __name__ == "__main__":
    main()
