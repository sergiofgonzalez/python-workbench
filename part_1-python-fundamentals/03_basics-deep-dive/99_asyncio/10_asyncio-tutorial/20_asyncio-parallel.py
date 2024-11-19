"""Illustrate how the event loop can run two tasks in parallel."""

import asyncio

from rich import print


async def say_hello_async() -> None:
    """Print delayed message after two seconds sleep."""
    await asyncio.sleep(2)
    print("[blue]Hello, async world![/blue]")


async def do_something_else() -> None:
    """Simulate some work being done in the background."""
    print("[green]working hard on another task!:[/green]", end=" ")
    await asyncio.sleep(1)
    print("[bold green]done![/bold green] yay! :dog:")


async def main() -> None:
    """Run the two coroutines defined above concurrently."""
    await asyncio.gather(say_hello_async(), do_something_else())


if __name__ == "__main__":
    asyncio.run(main())
