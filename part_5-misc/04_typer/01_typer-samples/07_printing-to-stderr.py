"""Using `rich` to print data."""

import typer
from rich.console import Console

err_console = Console(stderr=True)


def main() -> None:
    """CLI app entry point."""
    print("Here's a fabricated error:")
    err_console.print("You've exceeded your API quota limit for this month.")


if __name__ == "__main__":
    typer.run(main)
