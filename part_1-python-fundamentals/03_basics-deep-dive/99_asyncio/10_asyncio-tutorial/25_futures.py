"""Illustrates how to work with Futures and their methods."""

import asyncio

from rich import print


async def async_operation(future: asyncio.Future, data: str) -> None:
    """
    Simulate an async operation receiving a Future to communicate the result
    instead of directly returning the data from the coroutine.
    The result of the coroutine is driven by what's been sent in the data.
    """
    # Simulate
    await asyncio.sleep(1)

    if data == "success":
        future.set_result("Operation succeeded")
    else:
        future.set_exception(RuntimeError("Operation failed"))


def print_result_callback(future: asyncio.Future) -> None:
    """Sync function printing the result of the given Future."""
    try:
        print("[white bold]Callback:[/white bold]", future.result())
    except Exception as e:  # noqa: BLE001
        print("[white bold]Callback:[/white bold]:", e)


async def main() -> None:
    """Entry point of the app."""
    # Create a Future object
    future = asyncio.Future()

    # Bind the callback:
    #   print_result_callback will be invoked when the Future is done
    future.add_done_callback(print_result_callback)

    # Test the happy/failure path
    await async_operation(future, "some failure")

    # Check if the Future is done. If so, print result or handle exception
    if future.done():
        try:
            # this will raise if the Future completed with an exception
            print("[cyan bold]main:[/cyan bold]", future.result())
        except Exception as e:  # noqa: BLE001
            print("[cyan bold]main:[/cyan bold]", e)


if __name__ == "__main__":
    asyncio.run(main())
