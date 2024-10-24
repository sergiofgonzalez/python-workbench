"""A regular Python script converted to CLI app by typer."""

import typer

app = typer.Typer()


@app.command()
def hello(name: str) -> None:
    """Print a personalized greeting message."""
    print(f"Hello to {name}!")


@app.command()
def goodbye(name: str, formal: bool = False) -> None:
    """Print a personalized goodbye message."""
    if formal:
        print(f"Goodbye Ms. {name}. Have a good day.")
    else:
        print(f"Bye {name}")


if __name__ == "__main__":
    app()
