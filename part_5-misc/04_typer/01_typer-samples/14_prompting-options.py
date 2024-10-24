"""Asking for options."""

from typing import Annotated

import typer


# run it with python 14_prompting-options.py jason
def greeting(
    name: str,
    lastname: Annotated[
        str | None,
        typer.Option(prompt=True),
    ] = None,
) -> None:
    """Greet a given person."""
    print(f"Hello, {name}{' ' + lastname if lastname is not None else ''}!")


if __name__ == "__main__":
    typer.run(greeting)
