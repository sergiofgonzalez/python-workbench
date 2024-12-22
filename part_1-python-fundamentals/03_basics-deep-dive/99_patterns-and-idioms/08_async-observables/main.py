"""Illustrate how to inherit from EventEmitter to create observables."""

import asyncio
import re

import aiofiles

from events import EventEmitter


class FindRegex(EventEmitter):
    """Find matches in files using the Observer pattern."""

    def __init__(self, search_str: str) -> None:
        """Initialize instance."""
        super().__init__()
        self.filenames = []
        self.search_str = search_str
        self.regex = re.compile(search_str)

    def add_file(self, file_path: str) -> None:
        """Add a new file to the list of files to be scanned for matches."""
        self.filenames.append(file_path)

    def on(self, evt_name: str, cb: callable) -> None:
        """Register a new listener for the given event."""
        self.register_listener(evt_name, cb)

    async def find(self) -> None:
        """Find matches of the search_str in the given files."""
        for filename in self.filenames:
            await self._find_in_file(filename)

        # giving the background tasks a chance to execute
        await asyncio.gather(*list(self.background_tasks))

    async def _find_in_file(self, filename: str) -> None:
        """Find matches of the search_str in the given file."""
        try:
            async with aiofiles.open(filename) as file:
                self.emit("fileread", file.name)
                async for line in file:
                    if result := self.regex.search(line):
                        self.emit("found", file.name, line.strip(), result.group())
        except OSError as e:
            self.emit("error", str(e))

    def __repr__(self) -> str:
        """Developer-level representation of the instance."""
        return f"FindRegex({self.files=}, {self.search_str=})"


async def main() -> None:
    """Application entry point."""
    str_finder = FindRegex(r"aiofiles")
    str_finder.add_file("pyproject.toml")
    str_finder.add_file("uv.lock")
    str_finder.add_file("README.md")
    str_finder.add_file("non-existent-file.txt")
    str_finder.on("fileread", lambda file: print(f"About to scan {file}"))
    str_finder.on(
        "found",
        lambda file, line, match: print(f"HIT: {file}: {match!r} found in {line!r}"),
    )
    str_finder.on(
        "error",
        lambda err_message: print(
            f"ERROR: error found while scanning for matches: {err_message}",
        ),
    )
    await str_finder.find()


if __name__ == "__main__":
    asyncio.run(main())
