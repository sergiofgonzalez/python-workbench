"""Application main program."""

import random
import time

from log_time import log_time


@log_time
def some_fn(wait_seconds: float | None = None) -> float:
    """Wait for given seconds, or for a random amount of time if time not given."""
    if not wait_seconds:
        wait_seconds = random.uniform(0.5, 3)  # noqa: S311
    print(f"Will wait for {wait_seconds} seconds.")
    time.sleep(wait_seconds)
    return wait_seconds


def main() -> None:
    """Application entry point."""
    print(some_fn())
    print("=" * 80)
    print(some_fn(2.5))


if __name__ == "__main__":
    main()
