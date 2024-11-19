"""Illustrate how to read multiple files in parallel."""

import asyncio
from pathlib import Path

import aiofiles


async def read_file_async(filepath: str) -> str:
    """Read a single file asynchronously."""
    async with aiofiles.open(filepath) as file:
        return await file.read()


async def read_all_async(*filepaths: str) -> list[str]:
    """Schedule the execution of multiple async reads and return the results."""
    tasks = [read_file_async(filepath) for filepath in filepaths]
    return await asyncio.gather(*tasks)


async def main() -> None:
    """Compute the longest python progam so far."""
    filepaths = list(Path().glob("*.py"))
    data = await read_all_async(*filepaths)
    lengths = [len(file_data) for file_data in data]
    max_length = max(lengths)
    max_file_index = lengths.index(max_length)
    print(f"Longest program so far: {max_length} ({filepaths[max_file_index]})")


if __name__ == "__main__":
    asyncio.run(main())
