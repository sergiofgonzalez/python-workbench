"""Illustrates how to evaluate race conditions in asyncio programs."""

import asyncio

vals: list[int] = []


async def get_some_data_from_io() -> list[int]:
    """Simulate an I/O operation that returns some data after a delay."""
    await asyncio.sleep(0.5)
    return [42, 43, 44]


async def fetcher() -> None:
    """Fetch data and append it to the shared list."""
    while True:
        io_data = await get_some_data_from_io()
        for io_item in io_data:
            vals.append(io_item)  # noqa: PERF402


async def monitor() -> None:
    """Monitor the length of the shared list."""
    while True:
        print(f"Length of vals: {len(vals)}")
        await asyncio.sleep(1)


async def main() -> None:
    """Async application entry point."""
    await asyncio.gather(fetcher(), monitor())


if __name__ == "__main__":
    # start the evt loop in the current thread and schedule main() to run.
    asyncio.run(main())
