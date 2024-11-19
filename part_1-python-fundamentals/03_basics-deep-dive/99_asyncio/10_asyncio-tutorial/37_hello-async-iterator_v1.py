"""Illustrate (again) how to create an async iterator."""

import asyncio
from random import randint

from rich import print


class RandomAsyncValue:
    """A class that implements an async iterator that returns random ints."""

    def __init__(self) -> None:
        """Initialize the class."""
        print("[yellow]RandomAsyncValue async iterator initialized")

    def __aiter__(self) -> "RandomAsyncValue":
        """Return the next value in the async iterator."""
        return self

    async def __anext__(self) -> int:
        """Return an awaitable thatn when waited will return the next value."""
        nxt_val = randint(1, 6)
        asyncio.sleep(0)
        return nxt_val


async def main() -> None:
    """Async entry point."""
    i = 0
    async for num in RandomAsyncValue():
        print(f"{i}: {num}")
        if i >= 10:  # noqa: PLR2004
            break
        i += 1


if __name__ == "__main__":
    # Start the event loop in the current thread
    asyncio.run(main())
