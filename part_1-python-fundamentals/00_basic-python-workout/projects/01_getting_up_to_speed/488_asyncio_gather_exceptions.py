"""Illustrates proper exception handling with asyncio gather."""

import asyncio

from rich import print  # noqa: A004


async def coro_that_raises() -> None:
    """Raise an exception after sleeping for 2 seconds."""
    await asyncio.sleep(2)
    msg = "An error occurred in coro_that_raises"
    raise RuntimeError(msg)


async def coro_that_returns() -> str:
    """Return a success message after sleeping for 3 seconds."""
    await asyncio.sleep(3)
    return "coro_that_returns completed successfully"


async def main() -> None:
    """Async application entry point."""
    print("[bold] === return_exceptions=False (default) === [/bold]")
    try:
        results = await asyncio.gather(
            coro_that_raises(),
            coro_that_returns(),
        )
        print(f"[bold]Results: {results}[/bold]")
    except RuntimeError as exc:
        print(f"[bold red]Caught an exception: {exc}[/bold red]")

    print("[bold] === return_exceptions=True === [/bold]")
    results = await asyncio.gather(
        coro_that_raises(),
        coro_that_returns(),
        return_exceptions=True,
    )
    for index, result in enumerate(results):
        if isinstance(result, Exception):
            print(f"[bold red]Task {index} raised an exception: {result}[/bold red]")
        else:
            print(f"[bold green]Task {index} returned: {result}[/bold green]")
    print("Printing results list:", results)

    # Demonstrate that other tasks continue to run even if one fails
    print("[bold] === Demonstrating continued execution === [/bold]")
    gather_future = asyncio.gather(
        coro_that_raises(),
        coro_that_returns(),
        return_exceptions=True,
    )
    print("[bold]Doing other work while tasks run...[/bold]")
    await asyncio.sleep(1)
    if not gather_future.done():
        print("[bold]Tasks are still running...[/bold]")
    await gather_future
    print("[bold]All tasks completed.[/bold]")
    if gather_future.done():
        results = gather_future.result()
        print("Final results from gather_future:", results)

    # The same is not true if return_exceptions is False
    gather_future = asyncio.gather(
        coro_that_raises(),
        coro_that_returns(),
        return_exceptions=False,
    )
    print("[bold]Doing other work while tasks run...[/bold]")
    await asyncio.sleep(1)
    if not gather_future.done():
        print("[bold]Tasks are still running...[/bold]")
    try:
        await gather_future
        print("[bold]All tasks completed.[/bold]")
    except RuntimeError as exc:
        print(f"[bold red]At least some task failed: {exc}[/bold red]")
    if gather_future.done():
        # Calling result() here will re-raise the exception from coro_that_raises
        try:
            results = gather_future.result()
            print("Final results from gather_future:", results)
        except RuntimeError as exc:
            print(
                "[bold red]Caught an exception when retrieving results:"
                f" {exc}[/bold red]",
            )


if __name__ == "__main__":
    # start the evt loop in the current thread and schedule main() to run.
    asyncio.run(main())
