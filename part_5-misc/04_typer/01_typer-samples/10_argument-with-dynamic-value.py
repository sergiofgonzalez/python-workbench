"""Argument with a dynamic value."""

import random
from typing import Annotated

import typer


def get_random_name() -> str:
    """Return a random name."""
    return random.choice(["Jason", "Marge", "Ben", "Florence"])


def greeting(
    name: Annotated[
        str | None,
        typer.Argument(default_factory=get_random_name),
    ],
) -> None:
    """CLI app entry point."""
    print(f"Hello, {name}!")


if __name__ == "__main__":
    typer.run(greeting)
