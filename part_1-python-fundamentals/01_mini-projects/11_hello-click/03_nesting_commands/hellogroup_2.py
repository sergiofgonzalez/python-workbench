import click


@click.group()
def cli():
    ...


@click.command()
def initdb():
    click.echo("Initializing the database")


@click.command()
def dropdb():
    click.echo("Dropping the database")


cli.add_command(initdb)
cli.add_command(dropdb)

if __name__ == "__main__":
    cli()
