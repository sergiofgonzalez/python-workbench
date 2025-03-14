"""Gzips a file using buffer mode."""

import asyncio
import gzip
import time
from pathlib import Path
from typing import Annotated

import aiofiles
import typer
from rich import print  # noqa: A004


async def async_gzip_file(filename: Path) -> None:
    """Gzips the given filename using non-blocking I/O."""
    async with (
        aiofiles.open(filename, mode="rb") as infile,
        aiofiles.open(f"{filename}.gz", mode="wb") as outfile,
    ):
        bytes_data = await infile.read()
        await outfile.write(gzip.compress(bytes_data))
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
    asyncio.run(async_gzip_file(filename))
    print(f"Process took {time.perf_counter() - start:.3f} seconds.")


if __name__ == "__main__":
    typer.run(gzip_file)
