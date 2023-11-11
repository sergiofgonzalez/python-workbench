import click
from pprint import pprint


@click.group()
@click.option("--debug/--no-debug", default=False)
@click.pass_context
def cli(ctx, debug):
    pprint(ctx)
    ctx.ensure_object(dict)
    print(f"len(ctx.obj)={len(ctx.obj)}")
    for key, val in ctx.obj.items():
        print(f"{key}={val}")
    ctx.obj["DEBUG"] = debug


@cli.command()
@click.pass_context
def sync(ctx):
    click.echo(f"Debug is {'on' if ctx.obj['DEBUG'] else 'off'}")
    for key, val in ctx.obj.items():
        print(f"{key}={val}")


# When debugging it's better to include this:
if __name__ == "__main__":
    cli(obj={})     # Initialize the context with an empty dict