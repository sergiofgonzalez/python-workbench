"""Illustrate asyncio.wait usage."""

import asyncio
import random
import re

from rich import print  # noqa: A004


async def coro1(*, may_raise: bool = False) -> int:
    """Sleep for random amount of seconds and might fail with RuntimeError."""
    # Get the current task name to assign a color for logging
    task_name = asyncio.current_task().get_name()  # ty:ignore[possibly-missing-attribute]
    match = re.match(r"\w+-(?P<task_idx>\d+)", task_name)
    color = int(match.group("task_idx")) + 1 if match else 0

    delay = random.randint(0, 5)  # noqa: S311
    print(
        f"[color({color})]coro1(): {task_name}: sleeping for {delay} seconds"
        f"[/color({color})]",
    )

    await asyncio.sleep(delay)
    if may_raise and random.randint(0, 10) > 8:  # noqa: PLR2004, S311
        print(
            f"[color({color})]coro1(): {task_name}: will raise[/color({color})]",
        )
        msg = f"coro1 ({task_name}) encountered an error"
        raise RuntimeError(msg)
    return delay


async def main() -> None:  # noqa: C901, PLR0912, PLR0915
    """Async application entry point."""
    # Scenario 1: wait for all tasks until completion (no timeout), potential failures
    tasks = [
        asyncio.create_task(coro1(may_raise=True), name=f"randsleep-{i}")
        for i in range(5)
    ]
    done, pending = await asyncio.wait(tasks, return_when=asyncio.ALL_COMPLETED)
    print(f"[green]Done tasks: {len(done)=}; {len(pending)=}[/green]")
    for task in done:
        try:
            result = task.result()
            print(
                f"[green]{task.get_name()}: completed successfully with result "
                f"{result}[/green]",
            )
        except Exception as e:  # noqa: BLE001
            print(
                f"[red]{task.get_name()}: raised an exception: {e}[/red]",
            )
    if pending:
        print(f"[yellow]Pending tasks: {pending}[/yellow]")
        for task in pending:
            print(f"[yellow]{task.get_name()}[/yellow]")
    else:
        print("[green]No pending tasks[/green]")
    print("=" * 40)

    # Scenario 2: wait for all tasks until completion (with timeout), potential failures
    # Note that tasks are not cancelled when timeout occurs
    tasks = [
        asyncio.create_task(coro1(may_raise=True), name=f"randsleep-{i}")
        for i in range(5)
    ]
    done, pending = await asyncio.wait(
        tasks,
        return_when=asyncio.ALL_COMPLETED,
        timeout=3,
    )
    print(f"[green]Done tasks: {len(done)=}; {len(pending)=}[/green]")
    for task in done:
        try:
            result = task.result()
            print(
                f"[green]{task.get_name()}: completed successfully with result "
                f"{result}[/green]",
            )
        except Exception as e:  # noqa: BLE001
            print(
                f"[red]{task.get_name()}: raised an exception: {e}[/red]",
            )
    if pending:
        print(f"[yellow]Pending tasks: {len(pending)}[/yellow]")
        for task in pending:
            print(f"[yellow]{task.get_name()}[/yellow]")
        print("[green]Awaiting pending tasks to gather results...[/green]")
        results = await asyncio.gather(*pending, return_exceptions=True)
        print("[yellow]Results after timeout:[/yellow]")
        for task, result in zip(pending, results, strict=True):
            if isinstance(result, Exception):
                print(
                    f"[red]{task.get_name()}: raised an exception: {result}[/red]",
                )
            else:
                print(
                    f"[green]{task.get_name()}: completed successfully with result "
                    f"{result}[/green]",
                )

    else:
        print("[green]No pending tasks[/green]")
    print("=" * 40)

    # Scenario 3: wait for the first completed task (custom condition)
    tasks = [
        asyncio.create_task(coro1(may_raise=True), name=f"randsleep-{i}")
        for i in range(5)
    ]
    done, pending = await asyncio.wait(
        tasks,
        return_when=asyncio.FIRST_COMPLETED,
        timeout=3,
    )
    print(f"[green]Done tasks: {len(done)=}; {len(pending)=}[/green]")
    for task in done:
        try:
            result = task.result()
            print(
                f"[green]{task.get_name()}: completed successfully with result "
                f"{result}[/green]",
            )
        except Exception as e:  # noqa: BLE001
            print(
                f"[red]{task.get_name()}: raised an exception: {e}[/red]",
            )
    if pending:
        print(f"[yellow]Pending tasks: {len(pending)}[/yellow]")
        for task in pending:
            print(f"[yellow]{task.get_name()}[/yellow]")
        print("[green]Awaiting pending tasks to gather results...[/green]")
        results = await asyncio.gather(*pending, return_exceptions=True)
        print("[yellow]Results after timeout:[/yellow]")
        for task, result in zip(pending, results, strict=True):
            if isinstance(result, Exception):
                print(
                    f"[red]{task.get_name()}: raised an exception: {result}[/red]",
                )
            else:
                print(
                    f"[green]{task.get_name()}: completed successfully with result "
                    f"{result}[/green]",
                )

    else:
        print("[green]No pending tasks[/green]")
    print("=" * 40)

    # Scenario 4: wait for the first exception
    tasks = [
        asyncio.create_task(coro1(may_raise=True), name=f"randsleep-{i}")
        for i in range(5)
    ]
    done, pending = await asyncio.wait(
        tasks,
        return_when=asyncio.FIRST_EXCEPTION,
    )
    print(f"[green]Done tasks: {len(done)=}; {len(pending)=}[/green]")
    for task in done:
        try:
            result = task.result()
            print(
                f"[green]{task.get_name()}: completed successfully with result "
                f"{result}[/green]",
            )
        except Exception as e:  # noqa: BLE001
            print(
                f"[red]{task.get_name()}: raised an exception: {e}[/red]",
            )
    if pending:
        print(f"[yellow]Pending tasks: {len(pending)}[/yellow]")
        for task in pending:
            print(f"[yellow]{task.get_name()}[/yellow]")
        print("[green]Awaiting pending tasks to gather results...[/green]")
        results = await asyncio.gather(*pending, return_exceptions=True)
        print("[yellow]Results after timeout:[/yellow]")
        for task, result in zip(pending, results, strict=True):
            if isinstance(result, Exception):
                print(
                    f"[red]{task.get_name()}: raised an exception: {result}[/red]",
                )
            else:
                print(
                    f"[green]{task.get_name()}: completed successfully with result "
                    f"{result}[/green]",
                )

    else:
        print("[green]No pending tasks[/green]")


if __name__ == "__main__":
    # start the evt loop in the current thread and schedule main() to run.
    asyncio.run(main())
