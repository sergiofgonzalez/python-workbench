"""playing with asyncio."""

import asyncio
import time


async def delay(seconds: float) -> float:
    """Sleep asynchronously for the given amount of seconds."""
    await asyncio.sleep(seconds)
    return time.perf_counter()


async def main() -> None:
    """Async application entry point."""
    print("hello")
    start = time.perf_counter()
    end_ts = await delay(0.75)
    print(f"goodbye: {end_ts - start:.3f} seconds")


if __name__ == "__main__":
    asyncio.run(main())
