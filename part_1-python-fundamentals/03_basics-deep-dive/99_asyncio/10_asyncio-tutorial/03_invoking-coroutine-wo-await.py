"""A simple program that invokes coroutines without awaiting them."""

import asyncio
import sys
from pathlib import Path


async def create_file_async(name: str) -> None:
    """Create a file."""
    with Path.open(Path(name), "w") as file:
        file.write(f"Hello, {name}!")


async def main() -> None:
    """Invoke create_file three times without awaiting."""
    # using asyncio.gather without awaiting the results will schedule
    # the coroutines but not wait for their completion, which can lead to
    # unexpected results
    asyncio.gather(
        create_file_async("file_001.txt"),
        create_file_async("file_002.txt"),
        create_file_async("file_003.txt"),
    )

    # calling the coroutines without awaiting them triggers a RuntimeWarning
    # create_file_async("file_001.txt")
    # create_file_async("file_002.txt")
    # create_file_async("file_003.txt")


if __name__ == "__main__":
    asyncio.run(main())
