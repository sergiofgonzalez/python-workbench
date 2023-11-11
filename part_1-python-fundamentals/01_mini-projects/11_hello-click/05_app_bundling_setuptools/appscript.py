import click


@click.command()
def cli():
    click.echo("Hello, world!")


# Look ma, no if __name__ == "__main__"
