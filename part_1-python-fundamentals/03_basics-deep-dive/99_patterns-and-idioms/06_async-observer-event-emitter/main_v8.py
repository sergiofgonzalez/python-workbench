"""Illustrate the Observer pattern implemented in Python."""

import asyncio
import re

import aiofiles


class EventEmitter:
    """The subject of the Observer pattern."""

    def __init__(self) -> None:
        """Initialize an EventEmitter object."""
        self.listeners: dict[str, list[callable]] = {}
        self.background_tasks = set()

    def register_listener(self, evt_name: str, cb: callable) -> None:
        """Register a new observer (listener) in this event emitter."""
        if evt_name not in self.listeners:
            self.listeners[evt_name] = [cb]
        else:
            self.listeners[evt_name].append(cb)

    def emit(self, evt_name: str, *args: tuple, **kwargs: dict) -> None:
        """Fire an event by name with the given details."""
        for cb in self.listeners.get(evt_name, []):
            if asyncio.iscoroutinefunction(cb):
                task = asyncio.create_task(cb(*args, **kwargs))
                self.background_tasks.add(task)
                task.add_done_callback(self.background_tasks.discard)
            else:
                cb(*args, **kwargs)

    def remove_listener(self, evt_name: str, cb: callable) -> None:
        """Remove listener for the given event."""
        if evt_name in self.listeners:
            self.listeners[evt_name].remove(cb)
        else:
            msg = "No such event registered in this event emitter."
            raise ValueError(msg)


class RegexFinder(EventEmitter):
    """Class the implements the Observer pattern to find strings in files."""

    def __init__(self, files: list[str], search_str: str) -> None:
        """Initialize RegexFinder instance."""
        self.files = files
        self.search_str = search_str
        self.regex = re.compile(self.search_str)
        super().__init__()

    async def _search_in_file(self, filename: str) -> None:
        """Run the search process on a given file."""
        try:
            async with aiofiles.open(filename) as file:
                self.emit("fileread", file.name)
                async for line in file:
                    if result := self.regex.search(line):
                        self.emit("found", file.name, line.strip(), result.group())
        except OSError as e:
            self.emit("error", str(e))

    async def run(self) -> None:
        """Run the search notifying the corresponding listeners through events."""
        for file in self.files:
            await self._search_in_file(file)
        # giving the background tasks a chance to execute
        await asyncio.gather(*list(self.background_tasks))


async def async_cb(file: str) -> None:
    """Async callback to be used in the EventEmitter."""
    await asyncio.sleep(2.5)
    print(f"Async: scanning {file!r}")


async def main() -> None:
    """Application entry point."""
    find_regex = RegexFinder(
        ["pyproject.toml", "file.txt", "package.json"],
        r"(H|h)ello",
    )

    find_regex.register_listener(
        "fileread",
        async_cb,
    )
    find_regex.register_listener(
        "fileread",
        lambda file: print(f"Scanning {file!r}"),
    )
    find_regex.register_listener(
        "error",
        lambda err_msg: print(f"An error was found: {err_msg!r}"),
    )
    find_regex.register_listener(
        "found",
        lambda file, line, match: print(f"{file!r}: Matched {match!r} in {line!r}"),
    )
    await find_regex.run()


if __name__ == "__main__":
    asyncio.run(main())
