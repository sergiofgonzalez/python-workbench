"""Illustrate proper error management when using CPS in Python."""

import asyncio
import json
from collections.abc import Callable

import aiofiles


def get_when_done_cb(*obj_keys: str) -> Callable[[asyncio.Task], None]:
    """Return a callback parameterized to read the corresponding key."""

    def when_unmarshalled_fn(task: asyncio.Task) -> None:
        """Actions performed when file contents are unmarshalled."""
        if not task.cancelled():
            if e := task.exception():
                print(f">>> (when_unmarshalled): error caught: {e}")
            else:
                val = task.result()
                obj_keys_list = list(obj_keys)
                while obj_keys_list:
                    key = obj_keys_list.pop(0)
                    val = val.get(key)
                    if not val:
                        break
                if val:
                    print(f"{val=}")
                else:
                    msg = f"Could not retrieve value: keys: {obj_keys}"
                    raise ValueError(msg)
        else:
            print(">>> when_unmarshalled: task was cancelled")

    return when_unmarshalled_fn


async def get_json_obj(filename: str) -> dict[any, any]:
    """Unmarshall a JSON object from the given filename."""
    async with aiofiles.open(filename) as file:
        json_str = await file.read()
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


def handle_cb_exception(
    _: asyncio.AbstractEventLoop,
    context: dict[str, any],
) -> None:
    """Deal with an exception raised within a callback."""
    msg = context.get("exception", context["message"])
    print(
        f">>> (handle_cb_exception): an error was caught in the callback: {msg}",  # noqa: E501
    )


async def main() -> None:
    """Application entry point."""
    # Set the global exception handler
    loop = asyncio.get_event_loop()
    loop.set_exception_handler(handle_cb_exception)

    # # Happy path: single key
    # print_scenario_separator("Happy path one key")
    # await read_json("file_ok.json", get_when_done_cb("devDependencies"))

    # # Happy path: several keys
    # print_scenario_separator("Happy path several keys")
    # await read_json(
    #     "file_ok.json",
    #     get_when_done_cb("devDependencies", "eslint"),
    # )

    # Key related problem: single key
    # Errors in the callback are not caught while awaiting, but the program
    # keeps executing.
    print_scenario_separator("One key error")
    try:
        await read_json("file_ok.json", get_when_done_cb("nonExistentKey"))
    except (OSError, ValueError) as e:
        print(f">>> (main): error caught: {e}")

    # Key related problem: single key
    # Errors in the callback are not caught while awaiting, but the program
    # keeps executing.
    # print_scenario_separator("Several keys error")
    # try:
    #     await read_json(
    #         "file_ok.json",
    #         get_when_done_cb("devDependencies", "nonExistentKey"),
    #     )
    # except (OSError, ValueError) as e:
    #     print(f">>> (main): error caught: {e}")

    # # File related problem
    # # + Exception is raised when awaiting the coroutine
    # # + Exception is re-raised in the callback
    # print_scenario_separator("File not found")
    # try:
    #     await read_json(
    #         "file_not_found.json",
    #         get_when_done_cb("devDependencies", "eslint"),
    #     )
    # except (OSError, ValueError) as e:
    #     print(f">>> (main): error caught: {e}")

    # # JSON parsing related problem
    # # + Exception is raised when awaiting the coroutine
    # # + Exception is re-raised in the callback
    # print_scenario_separator("JSON parsing error")
    # try:
    #     await read_json(
    #         "file_err.txt",
    #         get_when_done_cb("devDependencies", "eslint"),
    #     )
    # except (OSError, ValueError) as e:
    #     print(f">>> (main): error caught: {e}")


if __name__ == "__main__":
    asyncio.run(main())
