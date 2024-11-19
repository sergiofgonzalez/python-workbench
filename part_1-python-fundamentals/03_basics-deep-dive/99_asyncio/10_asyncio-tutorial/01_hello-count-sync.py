"""A simple program that illustrates asyncio concurrency: sync version."""


import time
from pathlib import Path


def count() -> None:
    """Print one, sleep for one second, then print two."""
    print("One Mississippi")
    time.sleep(1)
    print("Two Mississippi")
    time.sleep(1)
    print("Three Mississippi")
    time.sleep(1)


def main() -> None:
    """Invoke count three times synchronously."""
    count()
    count()
    count()


if __name__ == "__main__":
    s = time.perf_counter()
    main()
    elapsed = time.perf_counter() - s
    print(f"{Path(__file__).name} executed in {elapsed:0.3f} seconds")
