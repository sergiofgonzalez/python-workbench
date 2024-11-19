"""Illustrate (again) how to create an async iterator."""

import asyncio
from random import randint

from rich import print


class RandomAsyncValue:
    """A class that implements an async iterator that returns random ints."""

    def __init__(self, max_nums: int) -> None:
        """Initialize the class."""
        print("[yellow]RandomAsyncValue async iterator initialized")
        self.max_nums = max_nums
        self.counter = 0

    def __aiter__(self) -> "RandomAsyncValue":
        """Return the next value in the async iterator."""
        return self

    async def __anext__(self) -> int:
        """Return the next random int."""
        self.counter += 1
        if self.counter <= self.max_nums:
            return randint(1, 6)
        raise StopAsyncIteration


async def main() -> None:
    """Async entry point."""
    i = 0
    async for num in RandomAsyncValue(10):
        i += 1
        print(f"{i}: {num}")

    # you can also iterate manually instead of with async for
    it = RandomAsyncValue(10)
    for i in range(5):
        val = await anext(it)
        print(f"{i}: {val}")


if __name__ == "__main__":
    # Start the event loop in the current thread
    asyncio.run(main())
