import click


def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo("Version 0.1.0")
    ctx.exit()


@click.command()
@click.option(
    "--version",
    is_flag=True,
    callback=print_version,
    expose_value=False,
    is_eager=True,
)
@click.option("--name", required=True)
def hello(name):
    click.echo(f"Hello {name}!")
