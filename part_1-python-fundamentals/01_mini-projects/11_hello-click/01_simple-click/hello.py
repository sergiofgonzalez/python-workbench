import click


@click.command()
@click.option("--count", default=1, help="Number of greetings.")
@click.option("--name", prompt="Your name", help="The person to greet.")
def hello(count, name):
    """Simple program that greets NAME for a total COUNT times."""
    for _ in range(count):
        click.echo(f"Hello to {name}!")


if __name__ == "__main__":
    hello()
