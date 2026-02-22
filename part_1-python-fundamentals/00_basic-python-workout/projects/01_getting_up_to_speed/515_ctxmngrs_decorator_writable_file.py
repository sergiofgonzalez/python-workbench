"""Illustrates how to create a context manager using the contextlib.contextmanager decorator."""
from contextlib import contextmanager
import rich
import pathlib

@contextmanager
def writable_file(file_name: str):
    """A context manager that opens a file for writing and ensures it is properly closed."""
    rich.print(f"[yellow]>>> Opening file: {file_name}[/yellow]")
    path = pathlib.Path("data", "out_data", "tmp") / file_name
    file = path.open("w")
    file.write("### Header introduced by the context manager ###\n")
    try:
        yield file
    finally:
        file.write("### Footer introduced by the context manager ###\n")
        file.close()
        rich.print(f"[yellow]>>> Closed file: {file_name}[/yellow]")



def main() -> None:
    """Application entry point."""
    with writable_file("example.txt") as f:
        f.write("This is some example content.\n")
        f.write("This content is written by the consumer in a with block.\n")

if __name__ == "__main__":
    main()
