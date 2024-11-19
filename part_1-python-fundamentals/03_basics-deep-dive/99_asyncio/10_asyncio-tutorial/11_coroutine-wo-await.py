"""Invoking a coroutine in event loop without awaiting it doesn't execute it."""

import asyncio
from pathlib import Path


async def write_file() -> None:
    """Write a file in a current dir as an indicator."""
    with Path.open("running.txt", "w") as file:
        file.write("Hello from a coroutine!")


async def main() -> None:
    """Application entry point."""
    write_file()
    print("Sleeping for 3 seconds...")
    await asyncio.sleep(3)


if __name__ == "__main__":
    # nothing happens
    asyncio.run(main())
