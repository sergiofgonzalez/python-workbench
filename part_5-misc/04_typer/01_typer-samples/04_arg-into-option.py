"""Converting a CLI argument into an option."""

import typer

# def greeting(name: str, last_name: str, *, formal: bool = False) -> None:
#     """Print a personalized greeting message."""
#     if formal:
#         print(f"Good day Ms. {name} {last_name}.!")
#     else:
#         print(f"Hey, Ms. {name} {last_name}!")


def greeting(name: str, *, last_name: str = "", formal: bool = False) -> None:
    """Print a personalized greeting message."""
    if formal:
        print(f"Good day Ms. {name} {last_name}.!")
    else:
        print(f"Hey, Ms. {name} {last_name}!")


if __name__ == "__main__":
    typer.run(greeting)
