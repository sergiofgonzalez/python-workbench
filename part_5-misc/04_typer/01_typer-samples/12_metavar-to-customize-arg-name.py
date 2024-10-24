"""Customizing the CLI arg name with `metavar`."""

from typing import Annotated

import typer


def greeting(
    name: Annotated[
        str | None,
        typer.Argument(
            metavar="username",
            help="The username",
        ),
    ],
    lastname: Annotated[
        str | None,
        typer.Argument(help="The last name of the person to greet"),
    ] = None,
) -> None:
    """Greet a given person."""
    print(f"Hello, {name}{' ' + lastname if lastname is not None else ''}!")


if __name__ == "__main__":
    typer.run(greeting)
