"""Task lifecycle."""

import asyncio
from collections.abc import Coroutine

from rich import print


async def handle_cancel(coro: Coroutine) -> str:
    """Wrap a coroutine in a try block to handle CancelledError."""
    try:
        return await coro
    except asyncio.CancelledError as e:
        print(f"[blue]CancelledError has been handled:[/blue]{e}")
        return "An attempt of cancelling me was requested"


async def my_coroutine(
    *,
    should_fail: bool,
    delay_seconds: int,
) -> str:
    """Illustrate the lifecycle of tasks using a dummy coroutine."""
    if should_fail:
        print(
            f"[blue]This coroutine will fail in {delay_seconds} sec[/blue]",
        )
    else:
        print(
            f"[blue]This coroutine will return in {delay_seconds} sec[/blue]",
        )
    await asyncio.sleep(delay_seconds)
    if should_fail:
        msg = "I was told to fail!"
        raise RuntimeError(msg)
    return "All went well!"


async def main() -> None:
    """Entry point for the async program."""
    # 1. Happy path for a task
    print("-" * 50)
    task = asyncio.create_task(my_coroutine(should_fail=False, delay_seconds=1))
    if not task.done():
        await task
    if not task.cancelled():
        try:
            result = task.result()
            print(f"The task was done with result: {result}")
        except Exception as e:  # noqa: BLE001
            print(f"The task failed with {e}")

    # 2. Exception path for a task
    # It will fail while awaiting, and again when checkin the results
    print("-" * 50)
    task = asyncio.create_task(my_coroutine(should_fail=True, delay_seconds=1))
    if not task.done():
        try:
            await task
        except Exception as e:  # noqa: BLE001
            print(f"The task failed while awaiting: {e}")
    if not task.cancelled():
        try:
            result = task.result()
            print(f"The task was done with result: {result}")
        except Exception as e:  # noqa: BLE001
            print(f"The task failed when checking results: {e}")

    # 3. Exception path for a task that was done:
    #   getting the exception explicitly
    # It will fail while awaiting, and again when checkin the results
    print("-" * 50)
    task = asyncio.create_task(my_coroutine(should_fail=True, delay_seconds=1))
    if not task.done():
        try:
            await task
        except Exception as e:  # noqa: BLE001
            print(f"The task failed while awaiting: {e}")
    if not task.cancelled():
        exception = task.exception()
        if not exception:
            print("The task did not fail")
        else:
            print("The task failed")

    # 4. Exception path for a task that was done with result:
    #   getting the exception explicitly
    # It will fail while awaiting, and again when checkin the results
    print("-" * 50)
    task = asyncio.create_task(my_coroutine(should_fail=False, delay_seconds=1))
    if not task.done():
        try:
            await task
        except Exception as e:  # noqa: BLE001
            print(f"The task failed while awaiting: {e}")
    if not task.cancelled():
        exception = task.exception()
        if not exception:
            print("The task did not fail")
            # we can safely get the result
            result = task.result()
            print(f"The task was done with result: {result}")
        else:
            print("The task failed")

    # 5. Cancelling a done task
    print("-" * 50)
    task = asyncio.create_task(my_coroutine(should_fail=False, delay_seconds=1))
    if not task.done():
        try:
            await task
        except Exception as e:  # noqa: BLE001
            print(f"The task failed while awaiting: {e}")
    was_cancelled = task.cancel("I want to cancel")
    print(f"{was_cancelled=}")

    # 5. Cancelling a task that has not been completed, and CancelledError is
    # not handled in the coroutine
    print("-" * 50)
    task = asyncio.create_task(my_coroutine(should_fail=False, delay_seconds=3))
    was_cancelled = task.cancel("I want to cancel")
    print(f"{was_cancelled=}")
    if not task.done():
        try:
            await task
        except asyncio.CancelledError as e:
            print(f"The task failed because was cancelled: {e}")
        except Exception as e:  # noqa: BLE001
            print(f"The task failed while awaiting (not CancelledError): {e}")

    # 6. Cancelling a task that has not been completed, and CancelledError is
    # handled in the coroutine
    print("-" * 50)
    coro = my_coroutine(should_fail=False, delay_seconds=3)
    task = asyncio.create_task(
        handle_cancel(coro),
    )
    # Give a chance to handle_cancel of being picked up by the event loop
    # If you remove the following line you'll get a RuntimeWarning because the
    # Task will never pass beyond the created state (i.e., won't be scheduled)
    await asyncio.sleep(1)
    was_cancelled = task.cancel("I want to cancel")
    print(f"{was_cancelled=}")
    if not task.done():
        try:
            await task
        except asyncio.CancelledError as e:
            print(f"The task failed because was cancelled: {e}")
        except Exception as e:  # noqa: BLE001
            print(f"The task failed while awaiting (not CancelledError): {e}")
    if not task.cancelled() and not task.exception():
        result = task.result()
        print(f"The task was done with result: {result}")
    else:
        print(f"The task was either failed or cancelled: {result}")


if __name__ == "__main__":
    asyncio.run(main())
