"""A regular Python script converted to CLI app by typer."""

import typer


def greeting(name: str) -> None:
    """Print a personalized greeting."""
    print(f"Hello to {name}!")


if __name__ == "__main__":
    typer.run(greeting)
