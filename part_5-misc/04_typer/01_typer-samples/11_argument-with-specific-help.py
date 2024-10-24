"""Argument with specific help."""

from typing import Annotated

import typer

# def greeting(
#     name: Annotated[
#         str | None,
#         typer.Argument(help="The name of the person to greet"),
#     ],
#     lastname: Annotated[
#         str | None,
#         typer.Argument(help="The last name of the person to greet"),
#     ] = None,
# ) -> None:
#     """Greet a given person."""
#     print(f"Hello, {name}{' ' + lastname if lastname is not None else ''}!")


# showing the default is sometimes ugly (especially when using None as the
# default value)
def greeting(
    name: Annotated[
        str | None,
        typer.Argument(
            help="The name of the person to greet",
            show_default="Jason (if nothing provided)",
        ),
    ] = "Jason",
    lastname: Annotated[
        str | None,
        typer.Argument(
            help="The last name of the person to greet",
            show_default=False,
        ),
    ] = None,
) -> None:
    """Greet a given person."""
    print(f"Hello, {name}{' ' + lastname if lastname is not None else ''}!")


if __name__ == "__main__":
    typer.run(greeting)
