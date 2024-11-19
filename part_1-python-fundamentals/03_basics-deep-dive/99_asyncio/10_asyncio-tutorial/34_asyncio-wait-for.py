"""Illustrate the use of asyncio.wait_for() with a timeout"""

import asyncio

from rich import print


async def my_coroutine(*, delay: int = 1, should_fail: bool = False) -> None:
    """Sleep asynchronously for the given time and might also fail."""
    print(
        f"[yellow]Will wait for {delay} seconds and {'will fail.' if should_fail else 'will not fail.'}"
    )  # nodqa: E501
    await asyncio.sleep(delay)
    if should_fail:
        print("[yellow]About to fail")
        msg = "I was told to fail"
        raise RuntimeError(msg)
    else:
        print("[yellow]Task completed without error")


async def main() -> None:
    """Async main coroutine."""
    # Task that doesn't fail and completes before timeout
    try:
        await asyncio.wait_for(my_coroutine(delay=3), timeout=5)
        print("Task completed")
    except TimeoutError:
        print("Task timed out before completing.")
    except RuntimeError as e:
        print(f"Task failed: {e}")

    # Task that doesn't fail but times out
    print("=" * 80)
    try:
        await asyncio.wait_for(my_coroutine(delay=3), timeout=2)
        print("Task completed")
    except TimeoutError:
        print("Task timed out before completing.")
    except RuntimeError as e:
        print(f"Task failed: {e}")

    # Task that fails before completing
    print("=" * 80)
    try:
        await asyncio.wait_for(
            my_coroutine(delay=3, should_fail=True), timeout=5,
        )
        print("Task completed")
    except TimeoutError:
        print("Task timed out before completing.")
    except RuntimeError as e:
        print(f"Task failed: {e}")


if __name__ == "__main__":
    # Start event loop in the current thread
    asyncio.run(main())
