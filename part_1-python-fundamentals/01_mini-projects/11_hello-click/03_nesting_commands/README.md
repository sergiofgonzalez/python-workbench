# Nesting commands with group


## hellogroup_1

Uses `@cli.command` decorators to identify the functions that implement the command.

## hellogroup_2

Uses `@click.command` decorators and `cli.add_command` to identify the functions that implement the command.

This can be useful in complex CLI apps in which you need to split the functions across different files.

