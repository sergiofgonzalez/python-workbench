"""Invokes a long-running task synchronously."""

import asyncio
import time


async def count(label: str) -> None:
    """Print one, sleep for one second, then print two."""
    print(f"{label}: One Mississippi")
    await asyncio.sleep(1)
    print(f"{label}: Two Mississippi")
    await asyncio.sleep(1)
    print(f"{label}: Three Mississippi")
    await asyncio.sleep(1)


async def main() -> None:
    """Invoke count three times synchronously."""
    start = time.perf_counter()
    await asyncio.gather(
        count("first"),
        count("second"),
        count("third"),
    )
    print(f"Execution took {time.perf_counter() - start:.2f} seconds")


if __name__ == "__main__":
    asyncio.run(main())
