"""Using multithreading with asyncio."""

import asyncio
import time

import requests


async def counter() -> None:
    """
    Coroutine that iterates over the numbers 0-9 sleeping for 1 msec (and
    thus yielding control to the event loop).
    """
    now = time.time()
    print("Started counter")
    for i in range(10):
        last = now
        await asyncio.sleep(0.001)
        now = time.time()
        print(f"{i}: was asleep for {now - last} sec")


async def main() -> None:
    """Run counter() async and make http request sync."""
    t = asyncio.get_event_loop().create_task(counter())

    await asyncio.sleep(0)

    def send_request() -> None:
        print("Sending HTTP request")
        r = requests.get("http://example.com")  # noqa: S113
        print(f"Got HTTP response with status {r.status_code}")

    await asyncio.get_event_loop().run_in_executor(None, func=send_request)

    await t


if __name__ == "__main__":
    asyncio.run(main())
