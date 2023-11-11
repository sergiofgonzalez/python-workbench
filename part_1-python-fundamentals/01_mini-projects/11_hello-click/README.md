# Hello, `click`!
> [`click`](https://github.com/pallets/click/) is a Python package for creating CLI interfaces in a composable way.

## Installation

`pip install -U click`

| NOTE: |
| :---- |
| `-U` stands for upgrade. |

## First example

You can find the most basic `click` example in [01_simple-click](01_simple-click/README.md)

```python
import click


@click.command()
@click.option("--count", default=1, help="Number of greetings.")
@click.option("--name", prompt="Your name", help="The person to greet.")
def hello(count, name):
    """Simple program that greets NAME for a total COUNT times."""
    for _ in range(count):
        click.echo(f"Hello to {name}!")


if __name__ == "__main__":
    hello()
```

## Basic Concepts

### Creating a command

Click is based on declaring commands through decorators.

A function becomes a Click command by decorating it with `@click.command()`:

```python
import click


@click.command()
def hello():
    click.echo("Hello, world!")


if __name__ == "__main__":
    hello()
```

The decorator converts the function into a `Command` which then can be invoked.

Thus, you'll be able to do:

```bash
python hello.py
```

But you'll also get the corresponding help page:

```bash
python hello.py --help
```

### Using `click.echo`

Note that the previous snippet uses `click.echo` rather than a regular `print`. The reason is to support consistent capabilities such as ANSI colors, different printing output when not using TTY, etc.

### Nesting commands

Commands can be attached to other commands of type `Group.` The idea is to allow arbitrary nesting of scripts.

There are two ways to do so. For simpler CLI apps, you can use decorators as below:

```python
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
```

And for more complex ones, in which the commands might be dispersed in different source files you can do the grouping programmatically:

```python
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
```

In both cases, you'll be able to invoke the tools as follows:

```bash
# initialize db
python dbmgmt initdb

# drop db
python dbmgmt dropdb

```

Note that in the latter case, instead of using `@group.command` decorator, we've used `@click.command` and then registered the group using `group.add_command(cmd_fn)`.

### Adding parameters to a command

To add parameters to a command, use the `@click.option()` and `@click.argument()` decorators

```python
import click


@click.command()
@click.argument("name")
@click.option("--count", default=1, help="number of greetings")
def hello(name, count):
    for _ in range(count):
        click.echo(f"Hello to {name}")


if __name__ == "__main__":
    hello()
```

```bash
# Show the CLI app's help
$ python helloargs.py --help
Usage: helloargs.py [OPTIONS] NAME

Options:
  --count INTEGER  number of greetings
  --help           Show this message and exit.

# Run with the argument only
$ python helloargs.py adri
Hello to adri

# Run with the arg and the option
$ python helloargs.py adri --count 3
Hello to adri
Hello to adri
Hello to adri
```

### Using Setuptools for better cross-platform integration

While traditionally, standalone Python files include:

```python
if __name__ == "__main__":
    hello()
```

it is recommended to switch to `setuptools` when using `click` because additional bundling and cross-platform capabilities for your CLI apps.

Additionally, it's recommended to write CLI apps as modules so that they become cross-platform tools instead of Unix-only CLI apps (e.g., `#!/usr/bin/env python` won't work on Windows).

In order to switch to this approach, you need the following:
+ your Python file for the CLI app
+ a `setup.py` file.

```python
"""appscript.py is the CLI's app main program"""
import click


@click.command()
def cli():
    click.echo("Hello, world!")
```

See how the `appscript.py` file doesn't include the `if __name__ == "__main__"`.

```python
"""setup.py is the Python file that contains the bundling info"""
from setuptools import setup

setup(
    name="appscript",
    version="0.1.0",
    py_modules=["yourscript"],
    install_requires=["Click"],
    entry_points={"console_scripts": ["appscript = appscript:cli"]},
)
```

The relevant part is the `entry_points` parameter. In the `console_scripts` you identify what is the name of the script that should be generated, the second part is the import path for the command: within the `appscript` Python file, the entry point is the `cli` function.

In order to bundle it, you just need to do:

```bash
# Use Python different from Linux OS one
conda activate base

# Create the virtualenv
python -m venv .venv --upgrade-deps

# Switch to virtualenv's Python
conda deactivate
source .venv/bin/active

# Install the package and bundle it
python -m pip install --editable .
```

The last command is the one that performs the bundling and enables you to do:

```bash
$ appscript
Hello, world!
```

#### Exercise

Create a CLI app that can be invoked with a NAME argument, and a `--count` optional parameter that prints a greeting message for the specified number of times.

The file that contains the application should be called `main.py`. Within it, the function that drives the logic should be called `hello_cli()`, and the app should be bundled as `hello` so that you can do:

```bash
$ hello "Jason Isaacs" --count 3
Hello to Jason Isaacs!
Hello to Jason Isaacs!
Hello to Jason Isaacs!
```

| NOTE: |
| :---- |
| See [e01_app_bundling_hello](e01_app_bundling_hello/) for the solution. |

### Scripts in Packages

If your script becomes large enough, you might want to switch over to a Python package approach.

You have an example in [06: App Bundling with Packages](06_app_bundling_packages/)

### Parameters

Click supports two types of parameters for scripts: options and arguments:
+ **options** are optional parameters
+ **arguments** must be super specific (such as the `NAME` in our previous hello apps), and almost always need to have a value. They can do a lot less than options.

The following features are only available for options (intentionally):
+ automatic prompting when input is missing.
+ act as flags.
+ values can be pulled from environment variables.
+ fully documented in the help page (note that arguments are NOT, that's why they need to be clearly understood and specific, as our `NAME` argument).

On the other hand, arguments can accept an arbitrary number of values. Options can accept a fixed number of arguments (defaults to 1), or they can be specified multiple times when using Multiple Options.

Parameters can be of different types. Each type comes with a set of behaviors:

+ `click.STRING`: the default parameter type which indicates Unicode strings.
+ `click.INT`: integers
+ `click.FLOAT`: floats
+ `click.BOOL`: parameter that accepts only boolean values. Automatically used for boolean flags. The string values `"1"`, `"true"`, `"t"`, `"yes"`, `"y"`, and `"on"` are automatically converted to `True`. Conversely, `"0"`, `"false"`, `"f"`, `"no"`, `"n"`, and `"off"` are automatically converted to `False`.
+ `click.UUID`: UUID values which are represented as `uuid.UUID`.
+ `click.File`: File decared for reading or writing.
+ `click.Path`: Similar to `File` but returns the filename instead of an open file. Various checks can be enabled to validate that it exists, that the corresponding path should be resolved, etc.
+ `click.Choice`: Allows the value to be checked agains a fixed set of supported values, which must be string.
+ `click.IntRange`: Allows a `click.INT` to a range of accepted values.
+ `click.FloatRange`: Allows a `click.FLOAT` to a range of accepted values.
+ `click.DateTime`: Converts date strings into datetime objects.

Note that custom parameter types can be implemented by subclassing `click.ParamType`.

Both types of parameters (options and arguments) have a name that will be used as the Python argument name when calling the decorated function with values.

Arguments take only one positional name. Options can have many names that may be prefixed with one or two dashes. Names with one dash are parsed as short options, names with two are parsed as long options. The prefix is removed and dashes in the middle are converted to underscores to get the Python argument name.

#### Exercise: examples with several params

Mimic the parameters needed for randfpck using Click parameters.

See [e02_randfpck](e02_randfpck_params/)

#### Implementing a Custom Type

To implement a custom type, you need to subclass the `ParamType` class. Override the `convert()` method to convert the value from a string to the correct type.

#### Options

The following snippets are self-explanatory:

```python
# option with a default value
@click.command()
@click.option("--n", default=1)
def dots(n):
    click.echo('_' * n)
```

```python
# required option of a given type
@click.command()
@click.option("--n", required=True, type=int)
def dots(n):
    click.echo('_' * n)
```

```python
# using a reserved word as a parameter
@click.command()
@click.option("--from", "-f", "from_")
def reserved_param_name(from_):
    ...
```

```python
# showing the default value in help
@click.command()
@click.option("--n", default=1, show_default=True)
def dots(n):
    click.echo('_' * n)
```

```python
# boolean flags (the default remains hidden if default value is False)
@click.command()
@click.option("--n", default=1, show_default=True)
@click.option("--gr", is_flag=True, show_default=True, default=False, help="Greet the world.")
@click.option("--br", is_flag=True, show_default=True, default=True, help="Add a thematic break.")
def dots(n):
    click.echo('_' * n)
```

##### Multi Value Options

For options, only a fixed number of arguments are supported. This can be configured by the `nargs` parameter. The values collected will be stored as a tuple.

```python
@click.command()
@click.option("--pos", nargs=2, type=float)
def findme(pos):
    a, b = pos
    ...
```

You can also instead of `nargs` specified the different multi-value options you're expecting as a tuple. This will allow you to get different types for the same option:

```python
@click.command()
@click.option("--item", type=(str, int))
def putitem(item):
    name, id = item
    ...
```

##### Multiple Options

Is it also possible to use the `multiple` flag to a allow a certain option to be specified any number of times:

```python
@click.command()
@click.option("--message", "-m", multiple=True)
def multi(message):
    click.echo("\n".join(message))
```

##### Counting

You can use the `count` flag to count an integer up:

```python
@click.command()
@click.option("--verbose", "-v", count=True)
def log(verbose):
    click.echo(f"Verbosity level: {verbose}")
```

```bash
$ log -vvv
Verbosity level: 3
```

##### Boolean Flags

Boolean flags are options that can be enabled or disabled. Click supports giving sensible names to those by defining the flag as two values separated by a slash:

```python
@click.command()
@click.option("--shout/--no-shout", default=False)
def multi(shout):
    ...
```

In certain cases, you might also want to use an off-switch:

```python
@click.command()
@click.option("--shout", is_flag=True)
def multi(shout):
    click.echo("\n".join(message))
```

##### Feature Switches

In addition to boolean flags, you can implement feature switches. These are implemented by setting multiple options to the same parameter name and defining a flag value:

```python
@click.command()
@click.option("--upper", "transformation", flag_value="upper")
@click.option("--lower", "transformation", flag_value="lower")
def info(transformation):
    click.echo(transformation)
```

So that you can do:

```bash
$ info --upper
upper

$ info --lower
lower
```

##### Choice Options

You can have a parameter to be a choice of a list of values using the `click.Choice` type:

```python
@click.command()
@click.option("--hash-type", type=click.Choice(["MD5", "SHA1"], case_sensitive=False))
def digest(hash_type):
    click.echo(hash_type)
```

So that you can do:

```bash
$ digest --hash-type=MD5
MD5

$ digest --hash-type=md5
MD5
```

##### Prompting

Click supports prompting the user for parameters that haven't been provided from the command line. This can be implement as follows:

```python
@click.command()
@click.option("--name", prompt=True)
def hello(name):
    ...
```

```bash
$ hello
Name:
```

```python
@click.command()
@click.option("--name", prompt="Your name please")
def hello(name):
    ...
```

```bash
$ hello
Your name please:
```

##### Password Prompts

Click also supports hidden prompts and asking for confirmation:

```python
@click.command()
@click.option("--password", prompt=True, hide_input=True, confirmation_prompt=True)
def cli(password):
    ...
```

Or with the shorthand:

```python
@click.command()
@click.password_option()
def cli(password):
    ...
```

```bash
$ cli
Password:
Repeat for confirmation:
```

##### Dynamic Defaults for Prompts

The `auto_envvar_prefix` and `default_map` options for the context allow the program to read option values from the environment or a configuration file.

Those options override the prompting mechanism. If you still want to let the user configure the default value you can do so by supplying a callable as the default value:

```python
@click.command()
@click.option(
    "--username",
    prompt=True,
    default=lambda: os.environ.get("USER", "")
)
def hello(username):
    click.echo(f"Hello to {username}!")
```

You can also use `show_default` to make help show the default value:

```python
@click.command()
@click.option(
    "--username",
    prompt=True,
    default=lambda: os.environ.get("USER", ""),
    show_default="current user"
)
def hello(username):
    click.echo(f"Hello to {username}!")
```

```bash
# Prompting the user and giving the default option from the envvar
$ hellouser
Username [ubuntu]:
Hello, ubuntu!

# Passing the option through the command-line won't propmpt
$ hellouser --username sfg
Hello, sfg!
```

| EXAMPLE: |
| :------- |
| See [08_dynamic_defaults](08_dynamic_defaults/) for a runnable example. |

##### Callbacks and Eager Options

Sometimes you want a parameter to completely change the execution flow. For instance, you might want to have a `--version` parameter that prints out the version and exits.

| NOTE: |
| :---- |
| Click provides a `click.version_option()` to specifically handle that use case. The code below is only for demonstration purposes. |

In those cases you need to use two concepts: eager parameters and a callback:
+ An eager parameter is a parameter that is handled before others.
+ A callback is what is executed after the parameter is handled.

For instance, if `--version` was not eager, and your tool required a `--foo` parameter, you'd still need to provide `--foo` to interrogate the version.

A callback is invoked with three parameters: the current `Context`, the current `Parameter`, and the value. The context provides some useful features such as quitting the application and gives access to other already processed parameters.


The following example is our canonical hello application, which requires a `--name` parameter, but also supports a `--version` implemented as an eager parameter and with a callback:

```python
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
```

This can be invoked as:

```bash
# Regular invocation
$ hello-ver --name sfg
Hello sfg!

# Interrogate the version
$ hello-ver --version
Version 0.1.0
```


The `expose_value` prevents the `version` parameter from being passed to the callback. The `ctx.resilient_parsing` is applied to the context if Click wants to parse the command line without any destructive behavior that would change the execution flow. If that is the case, we simply return.

##### Yes Parameters

For dangerous operations, it's useful to ask a user for confirmation. This can be done by adding a boolean `--yes` flag and asking for confirmation if the user did not provide it and if they didn't, fail in the callback:

```python

def abort_if_false(ctx, param, value):
    if not value:
        ctx.abort()

@click.command()
@click.option(
    "--yes",
    is_flag=True,
    callback=abort_if_false,
    expose_value=False,
    prompt="Are you sure you want to drop the db?"
)
def dropdb():
    click.echo("Dropped all the tables from the DB")
```

Again, this combination has the following shorthand:

```python
@click.command()
@click.confirmation_option(
    prompt="Are you sure you want to drop the db?"
)
def dropdb():
    click.echo("Dropped all the tables from the DB")
```

When you invoke it it will look like:

```bash
$ dropdb
Are you sure you want to drop the db? [y/N]: n
Aborted!

$ dropdb
Are you sure you want to drop the db? [y/N]: y
Dropped all tables!

$ dropdb --yes
Dropped all tables!
```

##### Values from Environment Variables

Click supports reading option values from environment variables using the `auto_envvar_prefix`. This needs to be passed to the script that is invoked:

```python
@click.command()
@click.option("--username")
def greet(username):
    click.echo("Hello, {username}!")

if __name__ == "__main__":
    greet(auto_envvar_prefix="GREETER")
```

Thus, you can do:

```bash
$ export GREETER_USERNAME=sfg
$ greet
Hello, sfg!
```

You can also pull values from specific environment variables by defining the name of the environment variable on the option:

```python
@click.command()
@click.option("--username", envvar="USERNAME")
def greet(username):
    click.echo(f"Hello, {username}!")
```

```bash
$ export USERNAME=sfg
$ greet
Hello, sfg!
```

##### Accepting multiple values from environment values

Pulling multiple values from environment variables for options accepting multiple values is a bit more tricky. Click will invoke the `ParamType.split_envvar_value()` method to perform the splitting, which by default will split on whitespace, except for Paths and Files which will split by `:` (Linux) and `;` (Windows).

```python
@click.command()
@click.option("paths", "--path", envvar="PATHS", multiple=True, type=click.Path())
def perform(paths):
    for path in paths:
        click.echo(path)
```

```bash
$ export PATHS="./foo/bar:./test
$ perform
./foo/bar
./test
```

##### Other Prefix Characters

Click can deal with alternative characters other that `-`. While this is discouraged as it goes agains POSIX semantics, it can be useful under certain circumstances:

```python
@click.command()
@click.option("+w/-w")
def chmod(w):
    click.each(f"writable={w}")
```

```bash
$ chmod +w
writable=True
$ chmod -w
writable=False
```

##### Range Options

Both `IntRange` and `FloatRange` types can be used to ask for ints or floats in a particular range. You can omit `min` or `max` to make that side unbounded. The limits are included, but you can also use `min_open` and `max_open` to exclude the boundary.

The parameter `clamp` will make a value that is outside the range to be set to the boundary instead of failing:

```python
@click.command()
@click.option("--count", type=click.IntRange(0, 7, clamp=True))
@click.option("--digit", type=click.IntRange(0, 9))
def repeat(count, digit):
    click.echo(str(digit) * count)
```

```bash
# only 7 5's will be printed
$ repeat --count=100 --digit=5
5555555

$ repeat --count=6 --digit=12
Usage: repeat [OPTIONS]
...
```

##### Callbacks for Validation

If you want to apply custom validation logic, you can do this in the parameter callbacks.

Callbacks can both modify values and raise errors if validation fails.

```python
def validate_rolls(ctx, param, value):
    if isinstance(value, tuple):
        return value

    try:
        rolls, _, dice=value.partition("d")
        return int(dice), int(rolls)
    except ValueError:
        reaise click.BadParameter("format must be NdM")

@click.command()
@click.option(
    "--rolls",
    type=click.UNPROCESSED,
    callback=validate_rolls,
    default="1d6",
    prompt=True
)
def roll(rolls):
    sides, times = rolls
    click.echo(f"Rollin a {sides}-sided dice {times} time(s)")
```

```bash
$ roll --rolls=42
Usage roll [OPTIONS]
...

roll --rolls=2d12
Rolling a 12-sided dice 2 time(s)
```

##### Optional Value

Providing a value to an option can be made optional, in which case, in which case providing only the option's flag without a value will either show a prompt or use its `flag_value`:

```python
@click.command()
@click.option(
    "--name",
    is_flag=False,
    flag_value="Flag",
    default="Default"
)
def hello(name):
    click.echo(f"Hello, {name}!")
```

Setting `is_flag=False` and `flag_value=value` tells Click that the option can still be passed a value. The `flag_value` will be used only if the flag is given but not the value:

```bash
# not passed
$ hello
Hello, Default!

# passed without a value
$ hello --name
Hello, Flag!

# passed a value
$ hello --name sfg
Hello, sfg!
```

You can use `promt_required=False` to only show the prompt if the option's flag is given.

```bash
# Force prompt
$ hello --name
Name [Default]:
```

#### Arguments

Arguments are similar to options, but they are positional. They available features available for arguments are limited, due to their syntactical nature.

Click will not attempt to document arguments for you, so you should document them manually.

In its most basic form, an argument is a simple string argument, which is assumed to be of type string:

```python
@click.command()
@click.argument("filename")
def touch(filename):
    """Print FILENAME."""
    click.echo(filename)
```

##### Variadic Arguments

Arguments can be variadic, accepting a specific (or unlimited) number of arguments. This can be controlled with the `nargs` parameter. When set to `-1`, an unlimited number of arguments is accepted.

The value is then passed as a tuple.

```python
@click.command()
@click.argument("src", nargs=-1)
@click.argument("dst", nargs=1)
def copy(src, dst):
    """Move file SRC to DST."""
    for f_src in src:
        click.echo(f"move {f_src} to folder {dst}")
```

An it will work as:

```bash
$ copy foo.txt bar.txt my_folder
move foo.txt to folder my_folder
move bar.txt to folder my_folder
```

##### File Arguments

File arguments are very common. This section will explain how to properly deal with them. In particular, command line tools are more fun if they work with files the Unix way, accepting `-` as a special file that refers to stdin/stdout.

```python
@click.command()
@click.argument("input", type=click.File("rb"))
@click.argument("output", type=click.File("wb"))
def inout(input, output):
    """Copy contents of INPUT to OUTPUT."""
    while True:
        chunk = input.read(1024)
        if not chunk:
            break
        output.write(chunk)
```

And this can be invoked as:

```bash
$ inout - hello.txt
hello
^D

$ inout hello.txt -
hello
```

##### File Path Arguments

File Path arguments are also very common. You can introduce several checks such as existence so that you don't need to do that yourself.

```python
@click.command()
@click.argument("filename", type=click.Path(exists=True))
def touch(filename):
    """Print FILENAME if the file exists."""
```

```bash
$ touch hello.txt
hello.txt

$ touch missing.txt
Usage: touch [OPTIONS] FILENAME
...
Error: Invalid value for 'FILENAME': Path 'missing.txt' does not exist.
```

##### Environment Variables

Like options, arguments can also grab values from an environment variable. This is done using the `envvar` decorator attribute.

```python
@click.command()
@click.argument("src", envvar="SRC", type=click.File("r"))
def echo(src):
    """Print value of SRC environment variable."""
    click.echo(src.read())
```

And this works like:

```bash
$ export SRC=hello.txt
$ echo
Hello, World!
```

##### Option-like Arguments

Sometimes you might need to process arguments that look like options, such as files named `-foo.txt`.

To solve this, Click follows the POSIX style guidelines, which tells you to accept the string `--` as a separator for options and arguments. After the `--` marker, all further parameters will be accepted as arguments:

```python
@click.command()
@click.argument("files", nargs=-1, type=click.Path())
def touch(files):
    """Print all FILES file names."""
    for filename in files:
        click.echo(filename)
```

So that from the command line:

```bash
$ touch -- -foo.txt bar.txt
-foo.txt
bar.txt
```

### Commands and Groups

One of the most relevant features of Click is the concept of arbitrarily nesting command line utilities. This is implemented through the `Command` and `Group`.

#### Callback Invocation

Consider the following situation, in which the script is the only command.

```python
# tool.py

@click.group()
@click.option("--debug/--no-debug", default=False)
def cli(debug):
    click.echo(f"Debug mode is {'on' if debug else 'off'}")

@cli.command
def sync():
    click.echo("Syncing")
```

This creates a CLI app with a single command `sync` that accepts an option `--debug/--no-debug`.

Thus, this can be invoked as:

```bash
tool.py --debug sync
Debug mode is on
Syncing
```

#### Passing Parameters

Click strictly separates parameters between commands and subcommands. This means that options and arguments for a specific command have to be specified after the command name itself, but before any other command names.

This behavior can be observed with the predefined `--help` option. Let's assume we have a CLI program `tool.py`, containing a subcommand `sub`.

+ `tool.py --help` will return the help for the whole program.
+ `tool.py sub --help` will show the help page for the `sub` subcommand.
+ `tool.py --help sub` will print the help and abort before processing `sub`.


#### Using Contexts

Consider the following snippet:

```python
# tool.py

@click.group()
@click.option("--debug/--no-debug", default=False)
def cli(debug):
    click.echo(f"Debug mode is {'on' if debug else 'off'}")

@cli.command
def sync():
    click.echo("Syncing")
```

The group accepts a debug argument which is passed to its callback, but not to the `sync` command itself. The `sync` command only accepts its own arguments.

While this allows tools to act completely independent of each other, there'll be cases where one command will need to interact to a nested one. This can be done through the `Context`.

Each time a command is invoked, a new context is created and linked with the parent context. Contexts are passed to parameter callbacks together with the value automatically. Commands can ask for the context to be passed by marking themselves with the `@click.pass_context` decorator, and they'll receive the context as the first argument.

With the context you can build a program like this:

```python
@click.group()
@click.option("--debug/--no-debug", default=False)
@click.pass_context
def cli(ctx, debug):
    ctx.ensure_object(dict) # ensure ctx.obj exists and that is a dict
    ctx.obj["DEBUG"] = debug

@cli.command()
@click.pass_context
def sync(ctx):
    click.echo(f"Debug mode is {'on' if ctx.obj['DEBUG'] else 'off'}")
```

### Prompts

Option prompts are integrated into the option interface.

Additionally, you can manually ask for user input doing:

```python
value = click.prompt("Please enter a valid integer", type=int)
```

```python
value = click.prompt("Please enter a number", default=42.0)
```

Similarly, you can manually ask for confirmation prompts:

```python
if click.confirm("Do you want to continue?"):
    click.echo("Processing...")
```

It is also possible to abort the execution if the user does not confirm:

```python
click.confirm("Do you want to continue?", abort=True)
```


## Screencast and examples

See https://click.palletsprojects.com/en/8.1.x/quickstart/#screencast-and-examples