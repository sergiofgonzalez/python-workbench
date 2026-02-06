"""Illustrate how to use asyncio.gather()."""

import asyncio

from rich import print  # noqa: A004


async def coro1(delay: int) -> str:
    """Sleep for delay seconds."""
    print(f"[blue]coro1: About to sleep for {delay} seconds[/blue]")
    await asyncio.sleep(delay)
    print(f"[blue]coro1: Finished sleeping for {delay} seconds[/blue]")
    return f"coro1 completed after {delay} seconds"


async def coro2(delay: int, *, should_fail: bool = False) -> str:
    """Sleep for delay seconds and optionally fail."""
    print(
        f"[red]coro2: About to sleep for {delay} seconds and will"
        f"{' [bold]fail[/bold]' if should_fail else ' [bold]succeed[/bold]'}[/red]",
    )
    await asyncio.sleep(delay)
    if should_fail:
        msg = f"coro2 failed after {delay} seconds"
        raise RuntimeError(msg)
    print(f"[red]coro2: Finished sleeping for {delay} seconds[/red]")
    return f"coro2 completed after {delay} seconds"


async def main() -> None:  # noqa: C901, PLR0912, PLR0915
    """Async application entry point."""
    # All end well and no await on the future is required to get results
    gather_future = asyncio.gather(
        coro1(delay=2),
        coro2(delay=3, should_fail=False),
        coro2(delay=4, should_fail=False),
    )
    await coro1(delay=5)

    if not gather_future.done():
        print("[green]gather(): still running...[/green]")
        await gather_future  # wait for it to complete
    else:
        print("[green]gather(): already done without await![/green]")

    if gather_future.done():
        print("[green]gather(): done[/green]")
        try:
            results = gather_future.result()
            print(f"[green]gather(): results: {results}[/green]")
        except Exception as e:  # noqa: BLE001
            print(f"[red]gather(): at least a task raised an exception: {e}[/red]")
    print("=" * 40)

    # All end well but await on the future is required to get results
    gather_future = asyncio.gather(
        coro1(delay=2),
        coro2(delay=3, should_fail=False),
        coro2(delay=6, should_fail=False),
    )
    await coro1(delay=4)

    if not gather_future.done():
        print("[green]gather(): still running...[/green]")
        await gather_future  # wait for it to complete
    else:
        print("[green]gather(): already done without await![/green]")

    if gather_future.done():
        print("[green]gather(): done[/green]")
        try:
            results = gather_future.result()
            print(f"[green]gather(): results: {results}[/green]")
        except Exception as e:  # noqa: BLE001
            print(f"[red]gather(): at least a task raised an exception: {e}[/red]")
    print("=" * 40)

    # the longest coro fails: you get the exception when asking for results
    gather_future = asyncio.gather(
        coro1(delay=2),
        coro2(delay=3, should_fail=False),
        coro2(delay=4, should_fail=True),
    )
    await coro1(delay=5)

    if not gather_future.done():
        print("[green]gather(): still running...[/green]")
        await gather_future  # wait for it to complete
    else:
        print("[green]gather(): already done without await![/green]")

    if gather_future.done():
        print("[green]gather(): done[/green]")
        try:
            results = gather_future.result()
            print(f"[green]gather(): results: {results}[/green]")
        except Exception as e:  # noqa: BLE001
            print(f"[red]gather(): at least a task raised an exception: {e}[/red]")
    print("=" * 40)

    # the coro in the middle fails: you get the exception when asking for results
    # but as soon as the failing coro is done the other coros are cancelled
    # you can see that the one with delay=6 does not complete
    gather_future = asyncio.gather(
        coro1(delay=2),
        coro2(delay=3, should_fail=True),
        coro2(delay=6, should_fail=False),
    )
    await coro1(delay=5)

    if not gather_future.done():
        print("[green]gather(): still running...[/green]")
        await gather_future  # wait for it to complete
    else:
        print("[green]gather(): already done without await![/green]")

    if gather_future.done():
        print("[green]gather(): done[/green]")
        try:
            results = gather_future.result()
            print(f"[green]gather(): results: {results}[/green]")
        except Exception as e:  # noqa: BLE001
            print(f"[red]gather(): at least a task raised an exception: {e}[/red]")
    print("=" * 40)

    # therefore, to avoid other coros being cancelled when one fails,
    # you need to use return_exceptions=True and then check whether the results
    # are exceptions or not
    gather_future = asyncio.gather(
        coro1(delay=2),
        coro2(delay=3, should_fail=True),
        coro2(delay=6, should_fail=False),
        return_exceptions=True,
    )
    await coro1(delay=5)

    if not gather_future.done():
        print("[green]gather(): still running...[/green]")
        await gather_future  # wait for it to complete
    else:
        print("[green]gather(): already done without await![/green]")

    if gather_future.done():
        print("[green]gather(): done[/green]")
        results = gather_future.result()
        print(f"[green]gather(): results: {results}[/green]")
        for idx, result in enumerate(results):
            if isinstance(result, Exception):
                print(f"[red]gather(): Task {idx} raised an exception: {result}[/red]")
            else:
                print(f"[green]gather(): Task {idx} result: {result}[/green]")
    print("=" * 40)


if __name__ == "__main__":
    # start the evt loop in the current thread and schedule main() to run.
    asyncio.run(main())
