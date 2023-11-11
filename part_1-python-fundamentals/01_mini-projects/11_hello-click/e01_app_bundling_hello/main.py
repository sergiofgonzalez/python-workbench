import click


@click.command()
@click.argument("name")
@click.option("--count", default=1, help="number of greetings.")
def cli_app(name, count):
    """Simple CLI app that greets NAME the given COUNT times."""
    for _ in range(count):
        click.echo(f"Hello to {name}!")
