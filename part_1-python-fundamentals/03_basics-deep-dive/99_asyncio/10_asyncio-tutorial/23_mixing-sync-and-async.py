"""Illustrate how to mix sync and async tasks."""

import asyncio
import time

from rich import print


def sync_task() -> None:
    """Simulate a long-running sync task."""
    print("[cyan][bold]sync[/bold]: Starting a slow sync task...[/cyan]")
    time.sleep(5)
    print("[cyan][bold]sync[/bold]: Completed slow task.[/cyan]")


async def async_wrapper() -> None:
    """Run a sync task in the event loop."""
    loop = asyncio.get_running_loop()
    # Run the sync task in a thread pool
    await loop.run_in_executor(None, sync_task)


async def async_task() -> None:
    """Simulate a long-running async task."""
    print("[green][bold]async[/bold]: Simulating an I/O task: starting[/green]")
    await asyncio.sleep(3)
    print("[green][bold]async[/bold]: I/O completed[/green]")


async def main() -> None:
    """Application entry point scheduling both async and sync tasks."""
    await asyncio.gather(async_wrapper(), async_task())


if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()
    print(f"[white bold]Took {end - start:0.3f} seconds.")
