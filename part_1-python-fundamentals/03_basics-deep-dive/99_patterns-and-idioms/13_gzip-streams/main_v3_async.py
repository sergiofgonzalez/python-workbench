"""Gzips a file using buffer mode."""

import asyncio
import gzip
import time
from pathlib import Path
from typing import Annotated

import aiofiles
import typer
from rich import print  # noqa: A004


async def gzip_file_async(filename: Path) -> None:
    """Gzips a file using non-blocking I/O."""
    async with (
        aiofiles.open(filename, mode="rb") as infile,
        aiofiles.open(f"{filename}.gz", mode="wb") as outfile,
    ):
        chunk = await infile.read(8192)
        done = False
        while not done:
            write_task = asyncio.create_task(outfile.write(gzip.compress(chunk)))
            read_chunk_task = asyncio.create_task(infile.read(8192))
            done = len(chunk) == 0
            _, chunk = await asyncio.gather(write_task, read_chunk_task)
    print(f"[bold white]{filename}[/bold white] => [green]{filename}.gz[/green]")


def gzip_file(
    filename: Annotated[
        Path,
        typer.Argument(
            exists=True,
            dir_okay=False,
            file_okay=True,
            readable=True,
            resolve_path=False,
            show_default=False,
            help="Path to the file to gzip",
        ),
    ],
) -> None:
    """Create a .gz file using a buffer mode."""
    start = time.perf_counter()
    asyncio.run(gzip_file_async(filename))
    print(f"File compressed in {time.perf_counter() - start:.3f} seconds.")


if __name__ == "__main__":
    typer.run(gzip_file)
