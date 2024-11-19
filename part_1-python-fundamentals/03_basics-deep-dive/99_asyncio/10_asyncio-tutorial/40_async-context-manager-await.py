"""Illustrate how to create and use a context manager."""

import asyncio

from rich import print


class AsyncContextManager:
    """Async context manager."""

    def __init__(self) -> None:
        """Async context manager constructor."""
        print("[bright_yellow]AsyncContextManager.init()")

    async def __aenter__(self) -> "AsyncContextManager":
        """Async context manager setup."""
        print("[bright_yellow]AsyncContextManager.__aenter__()")
        await asyncio.sleep(1)
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:  # noqa: ANN001
        """Async context manager tear down."""
        print("[bright_yellow]AsyncContextManager.__aexit__()")
        await asyncio.sleep(1)
        return self

    def greet(self) -> None:
        """Say hello."""
        print("Hello from the AsyncContextManager")


async def main() -> None:
    """Async entry point."""
    async with AsyncContextManager() as manager:
        print("[bright_green]In the async context manager block")
        manager.greet()
    print("[bright_green]Out of the async context manager block")


if __name__ == "__main__":
    # Start the event loop in the current thread
    asyncio.run(main())
