"""
A program that generates random integers in the range [0, 10] until one of
them exceeds a threshold.
The best way to understand how it works is to run it a few times.
"""

import asyncio
import random

ANSI_COLORS = (
    "\033[0m",  # End of color
    "\033[36m",  # Cyan
    "\033[91m",  # Red
    "\033[35m",  # Magenta
)


async def make_random(idx: int, threshold: int = 6) -> int:
    """
    Generate random int in the range [0, 10] until the generated number is
    greater than the given threshold.
    """
    print(f"{ANSI_COLORS[idx + 1]} Initiated make_random({idx}, {threshold}).")
    i = random.randint(0, 10)
    while i <= threshold:
        print(f"{ANSI_COLORS[idx + 1]} generated {i}: too low, retrying.")
        await asyncio.sleep(idx + 1)
        i = random.randint(0, 10)
    print(
        f"{ANSI_COLORS[idx + 1]} >>> finished: generated {i}.{ANSI_COLORS[0]}",
    )
    return i


async def main() -> tuple[int, int, int]:
    """
    Schedule the async execution of three instances of make_random() with
    different thresholds.
    """
    res = await asyncio.gather(*(make_random(i, 10 - i - 1) for i in range(3)))
    return res  # noqa: RET504


if __name__ == "__main__":
    random.seed(444)
    r1, r2, r3 = asyncio.run(main())
    print(f"{r1=}, {r2=}, {r3=}")
