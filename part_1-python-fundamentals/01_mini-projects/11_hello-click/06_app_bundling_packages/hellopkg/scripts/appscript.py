import click

from hellopkg.main import get_greeting


@click.command()
@click.argument("name")
@click.option("--count", default=1, help="The number of greetings.")
def cli(name, count):
    for _ in range(count):
        click.echo(get_greeting(name))
