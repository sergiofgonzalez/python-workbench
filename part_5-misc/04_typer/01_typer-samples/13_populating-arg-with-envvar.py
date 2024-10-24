"""Populating a CLI argument from an environment variable value."""

from typing import Annotated

import typer


# run it with AWESOME_NAME="jason" python 13_populating-arg-with-envvar.py
# see how the env var is hidden from the help screen in lastname
# you can check that with:
# $ AWESOME_NAME="json" AWESOME_LASTNAME="isaacs" \
# python 13_populating-arg-with-envvar.py
def greeting(
    name: Annotated[
        str | None,
        typer.Argument(envvar="AWESOME_NAME"),
    ],
    lastname: Annotated[
        str | None,
        typer.Argument(envvar="AWESOME_LASTNAME", show_envvar=False),
    ] = None,
) -> None:
    """Greet a given person."""
    print(f"Hello, {name}{' ' + lastname if lastname is not None else ''}!")


if __name__ == "__main__":
    typer.run(greeting)
