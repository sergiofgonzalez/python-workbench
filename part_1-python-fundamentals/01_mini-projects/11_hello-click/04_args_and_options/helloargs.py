import click


@click.command()
@click.argument("name")
@click.option("--count", default=1, help="number of greetings")
def hello(name, count):
    for _ in range(count):
        click.echo(f"Hello to {name}")


if __name__ == "__main__":
    hello()
