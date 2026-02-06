"""Illustrate how blocking the event loop affects asyncio programs performance."""

import asyncio
import time

import requests
import rich


async def counter() -> None:
    """Count to 0 to 9 cooperatively."""
    count = 0
    while True:
        print(f"Counter: {count}")
        count += 1
        start_ts = time.perf_counter()
        await asyncio.sleep(0.001)
        sleep_duration = time.perf_counter() - start_ts
        if count >= 10:  # noqa: PLR2004
            break
        if sleep_duration > 0.01:  # noqa: PLR2004
            rich.print(
                f"[red]Event loop was blocked in iteration {count}! Slept for {sleep_duration:.6f} seconds.[/red]",  # noqa: E501
            )



async def blocking_task_sync_lib() -> None:
    """Blocks the event loop by using a synchronous library."""
    response = requests.get("https://example.com", timeout=5)  # noqa: ASYNC210
    if response.status_code == requests.codes["ok"]:
        print("http://example.com responded with status 200")
    else:
        rich.print(
            f"[red]http://example.com responded with status {response.status_code}[/red]",  # noqa: E501
        )


async def main() -> None:
    """Async application entry point."""
    # Runing counter by itself
    await counter()
    print("=" * 40)

    # Running the blocking task by itself
    await blocking_task_sync_lib()
    print("=" * 40)

    # Mix them together to see the effect of blocking the event loop
    await asyncio.gather(counter(), blocking_task_sync_lib())
    print("=" * 40)


if __name__ == "__main__":
    # start the evt loop in the current thread and schedule main() to run.
    asyncio.run(main())
