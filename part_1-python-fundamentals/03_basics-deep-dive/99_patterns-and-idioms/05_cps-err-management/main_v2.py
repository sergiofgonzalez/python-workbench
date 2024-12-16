"""Illustrate proper error management when using CPS in Python."""

import asyncio
import json
from collections.abc import Callable
from pathlib import Path


def when_unmarshalled(task: asyncio.Task) -> None:
    """Actions performed when file contents are unmarshalled."""
    if not task.cancelled():
        if e := task.exception():
            print(f">>> (when_unmarshalled): error caught: {e}")
        else:
            obj = task.result()
            dev_dependencies = obj.get("devDependencies")
            if dev_dependencies:
                print(f"Development dependencies: {dev_dependencies}")
            else:
                print("No development dependencies found")
    else:
        print(">>> when_unmarshalled: task was cancelled")


def read_file_sync(filename: str) -> str:
    """Read the contents of a file using a blocking I/O operation."""
    with Path(filename).open("r") as file:
        return file.read()


async def get_json_obj(filename: str) -> dict[any, any]:
    """Unmarshall a JSON object from the given filename."""
    wrapped_coro = asyncio.to_thread(read_file_sync, filename)
    json_str = await wrapped_coro
    return json.loads(json_str)


async def read_json(
    filename: str,
    cb: Callable[[dict[any, any]], None],
) -> None:
    """Read given file and unmarshall its contents as a dict using CPS."""
    task = asyncio.create_task(get_json_obj(filename))
    task.add_done_callback(cb)
    if not task.done():
        await task


def print_scenario_separator(label: str) -> None:
    """Print scenario separator."""
    print(f"\n{'=' * 50}{label:^30}{'=' * 20}")


async def main() -> None:
    """Application entry point."""
    # Happy path
    print_scenario_separator("Happy path")
    await read_json("file_ok.json", when_unmarshalled)

    # File related problem
    # + Exception is raised when awaiting the coroutine
    # + Exception is re-raised in the callback
    print_scenario_separator("File not found")
    try:
        await read_json("file_not_found.json", when_unmarshalled)
    except (OSError, ValueError) as e:
        print(f">>> (main): error caught: {e}")

    # JSON parsing related problem
    # + Exception is raised when awaiting the coroutine
    # + Exception is re-raised in the callback
    print_scenario_separator("JSON parsing error")
    try:
        await read_json("file_err.txt", when_unmarshalled)
    except (OSError, ValueError) as e:
        print(f">>> (main): error caught: {e}")


if __name__ == "__main__":
    asyncio.run(main())
