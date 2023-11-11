import os

import click


@click.command()
@click.option(
    "--username",
    prompt=True,
    default=lambda: os.environ.get("USER", ""),
    show_default="current user",
)
def hello(username):
    click.echo(f"Hello, {username}!")
