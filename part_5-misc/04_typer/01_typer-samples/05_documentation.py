"""Adding custom documentation to the tool."""

import typer


def greeting(name: str, *, last_name: str = "", formal: bool = False) -> None:
    """
    Print a personalized greeting to NAME, optionally with a --last-name.

    If --formal is used, the greeting is more formal.
    """
    if formal:
        print(f"Good day Ms. {name} {last_name}.!")
    else:
        print(f"Hey, Ms. {name} {last_name}!")


if __name__ == "__main__":
    typer.run(greeting)
