import click

class BasedIntParamType(click.ParamType):
    """Implements an integer type that accepts hex and octal numbers in addition
    to normal integers, and converts them into regular integers.
    """
    name = "integer"

    def convert(self, value, param, ctx):
        if isinstance(value, int):
            return value

        try:
            if value[:2].lower() == "0x":
                return int(value[2:], 16)
            elif value[:1] == "0":
                return int(value, 8)
            return int(value, 10)
        except ValueError:
            self.fail(f"{value!r} is not a valid integer", param, ctx)

BASED_INT = BasedIntParamType()


@click.command()
@click.argument("num", type=BASED_INT)
def cli(num):
    """Converts a hex or octal NUM to a base-10 integer."""
    click.echo(num)
