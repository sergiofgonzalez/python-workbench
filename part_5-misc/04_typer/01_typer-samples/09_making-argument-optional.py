"""Making an argument optional."""

from typing import Annotated

import typer


def greeting(name: Annotated[str | None, typer.Argument()] = None) -> None:
    """CLI app entry point."""
    if name is None:
        print("Hello, stranger!")
    else:
        print(f"Hello, {name}!")


if __name__ == "__main__":
    typer.run(greeting)
