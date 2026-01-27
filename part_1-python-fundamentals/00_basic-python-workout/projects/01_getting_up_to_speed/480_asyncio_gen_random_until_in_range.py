"""Illustrates how to create a coroutine that generates numbers asynchronously."""

import asyncio
import random
import time

ANSI_COLORS = (
    "\033[0m",  # reset
    "\033[91m",  # red
    "\033[35m",  # magenta
    "\033[36m",  # cyan
    "\033[93m",  # yellow
)


async def make_random(idx: int, threshold: int = 6) -> int:
    """Generate random numbers until one greater than the threshold.

    Args:
        idx: An index to identify the caller.
        threshold: Establishes the boundary beyond which the random number is
            acceptable.

    Returns:
        The first random number greater than the threshold.

    """
    print(
        f"{ANSI_COLORS[idx]}Task {idx}: starting with threshold {threshold}{ANSI_COLORS[0]}",  # noqa: E501
    )
    while True:
        value = random.randint(0, 10)  # noqa: S311
        print(f"{ANSI_COLORS[idx]}Task {idx}: generated {value}{ANSI_COLORS[0]}")
        if value > threshold:
            print(f"{ANSI_COLORS[idx]}Task {idx}: accepted {value}{ANSI_COLORS[0]}")
            return value
        print(
            f"{ANSI_COLORS[idx]}Task {idx}: rejected {value}, retrying...{ANSI_COLORS[0]}",  # noqa: E501
        )
        await asyncio.sleep(idx + 1)


async def main() -> tuple[int, int, int]:
    """Application entry point."""
    result = await asyncio.gather(
        make_random(1, 9),
        make_random(2, 8),
        make_random(3, 7),
    )
    return result  # noqa: RET504


if __name__ == "__main__":
    random.seed(444)
    start_ts = time.perf_counter()
    res1, res2, res3 = asyncio.run(main())
    print(f"Results: {res1=}, {res2=}, {res3=}")
    print(f"Execution took {time.perf_counter() - start_ts:.2f} seconds")
