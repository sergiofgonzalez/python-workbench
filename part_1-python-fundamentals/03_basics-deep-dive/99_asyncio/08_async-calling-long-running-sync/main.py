"""Illustrates how calling is bad."""

import asyncio
import time

import requests


async def counter() -> None:
    """
    Coroutine that iterates over the numbers 0-9 sleeping for 1 msec (and
    thus yielding control to the event loop).
    """
    now = time.time()
    print("Counter started")
    for i in range(10):
        last = now
        # yields control to event loop
        await asyncio.sleep(0.001)
        now = time.time()
        print(f"{i}: was asleep for {now -last}s")


async def main() -> None:
    """Run counter() async and make http request sync."""
    task = asyncio.get_event_loop().create_task(counter())

    # yield control to event loop
    await asyncio.sleep(0)
    print("Sending HTTP request")
    r = requests.get("http://example.com")  # noqa: ASYNC210, S113
    print(f"Got HTTP response with status: {r.status_code}")

    await task


if __name__ == "__main__":
    asyncio.run(main())
