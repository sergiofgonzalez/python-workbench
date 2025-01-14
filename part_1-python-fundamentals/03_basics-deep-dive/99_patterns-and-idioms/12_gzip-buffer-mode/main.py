"""Gzips a file using buffer mode."""

import gzip
import time
from pathlib import Path
from typing import Annotated

import typer
from rich import print  # noqa: A004


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
    with (
        Path(filename).open("rb") as infile,
        Path(f"{filename}.gz").open("wb") as outfile,
    ):
        bytes_data = infile.read()
        outfile.write(gzip.compress(bytes_data))
    print(f"[bold white]{filename}[/bold white] => [green]{filename}.gz[/green]")
    print(f"Process took {time.perf_counter() - start:.3f} seconds.")


if __name__ == "__main__":
    typer.run(gzip_file)
