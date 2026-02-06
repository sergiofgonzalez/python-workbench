"""504_asyncio_run_in_executor_to_thread.py.

Illustrates how to use run_in_executor and to_thread to run blocking code in
in a separate asyncio thread.
"""

import asyncio
import time
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor

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
                f"[red]Event loop was blocked in iteration {count}! Slept for {sleep_duration:.3f} seconds.[/red]",  # noqa: E501
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


def send_request() -> None:
    """Blocks the event loop by using a synchronous library."""
    response = requests.get("https://example.com", timeout=5)
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

    # Run blocking task in a separate thread using run_in_executor
    loop = asyncio.get_running_loop()
    await asyncio.gather(counter(), loop.run_in_executor(None, send_request))
    print("=" * 40)

    # Run blocking task in a separate thread using to_thread
    await asyncio.gather(counter(), asyncio.to_thread(send_request))
    print("=" * 40)

    # Run blocking task in a separate thread using a non-default ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=2) as pool:
        loop = asyncio.get_running_loop()
        await asyncio.gather(counter(), loop.run_in_executor(pool, send_request))
    print("=" * 40)

    # Run blocking task in a separate thread using a non-default ProcessPoolExecutor
    with ProcessPoolExecutor(max_workers=2) as pool:
        loop = asyncio.get_running_loop()
        await asyncio.gather(counter(), loop.run_in_executor(pool, send_request))
    print("=" * 40)


if __name__ == "__main__":
    # start the evt loop in the current thread and schedule main() to run.
    asyncio.run(main())
