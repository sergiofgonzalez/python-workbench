"""Illustrates that when using asyncio.gather you work with a single Future."""

import asyncio

from rich import print


async def my_coroutine1(delay_sec: int) -> str:
    """Sleep async for the given number of seconds."""
    print(
        f"[blue][bold]my_coroutine1[/bold]: sleeping for {delay_sec} seconds[/blue]"
    )  # noqa: E501
    await asyncio.sleep(delay_sec)
    print("[blue][bold]my_coroutine1[/bold]: sleeping done[/blue]")
    return f"[blue]I waited for {delay_sec} second(s).[/blue]"


async def my_coroutine2(delay_sec: int, *, should_fail: bool = False) -> str:
    """Sleep async for the given number of seconds."""
    print(
        f"[yellow][bold]my_coroutine2[/bold]: sleeping for {delay_sec} seconds[/yellow]"
    )
    await asyncio.sleep(delay_sec)
    print("[yellow][bold]my_coroutine2[/bold]: sleeping done[/yellow]")
    if should_fail:
        msg = "I was told to raise"
        raise RuntimeError(msg)
    return f"[yellow]I waited for {delay_sec} second(s).[/yellow]"


async def main() -> None:
    """Entry point for async app."""
    futures = asyncio.gather(
        my_coroutine1(delay_sec=1),
        my_coroutine2(delay_sec=2),
        # Change should_fail=True to see what happens when one of the Futures
        # fail
        asyncio.create_task(
            my_coroutine2(delay_sec=3, should_fail=False),
        ),
    )
    # invoking asyncio.gather doesn't prevent us from sending other things to
    # the event loop
    await my_coroutine1(delay_sec=4)

    # you can use the result of asyncio.gather as a single future
    if futures.done():
        print("main(): futures completed")
    else:
        print("main(): not done yet - will await")
        try:
            await futures
        except Exception:  # noqa: BLE001
            print("main(): at least one of the Futures failed")

    try:
        results = futures.result()
    except Exception:  # noqa: BLE001
        print("main(): at least one of the Futures failed")
    else:
        for i, result in enumerate(results):
            print(f"{i}: {result}")


if __name__ == "__main__":
    asyncio.run(main())
