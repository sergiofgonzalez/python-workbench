import click


@click.group()
def cli():
    ...


@cli.command()
def initdb():
    click.echo("Initializing the database")


@cli.command()
def dropdb():
    click.echo("Dropping the database")


if __name__ == "__main__":
    cli()
