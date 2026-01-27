"""Invokes a long-running task synchronously."""

import time


def count(label: str) -> None:
    """Print one, sleep for one second, then print two."""
    print(f"{label}: One Mississippi")
    time.sleep(1)
    print(f"{label}: Two Mississippi")
    time.sleep(1)
    print(f"{label}: Three Mississippi")
    time.sleep(1)


def main() -> None:
    """Invoke count three times synchronously."""
    start = time.perf_counter()
    count("first")
    count("second")
    count("third")
    print(f"Execution took {time.perf_counter() - start:.2f} seconds")


if __name__ == "__main__":
    main()
