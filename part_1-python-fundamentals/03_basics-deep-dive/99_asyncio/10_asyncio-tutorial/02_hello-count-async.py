"""A simple program that illustrates asyncio concurrency: async version."""

import asyncio
import time
from pathlib import Path


async def count() -> None:
    """Print one, sleep for one second, then print two."""
    print("One Mississippi")
    await asyncio.sleep(1)
    print("Two Mississippi")
    await asyncio.sleep(1)
    print("Three Mississippi")
    await asyncio.sleep(1)


async def main() -> None:
    """Invoke count three times synchronously."""
    await asyncio.gather(count(), count(), count())


if __name__ == "__main__":
    s = time.perf_counter()
    asyncio.run(main())
    elapsed = time.perf_counter() - s
    print(f"{Path(__file__).name} executed in {elapsed:0.3f} seconds")
