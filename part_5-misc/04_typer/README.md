# Typer
> a library for building CLI applications


## Intro

Typer is both a library for building CLI applications based on Python type hints, and also a command line tool to run scripts as CLI apps (even if they don't use `typer` library internally).

## Typer features

### CLI Arguments

A CLI argument is a parameter passed in some specific order to the CLI application. By default, they are required.

In Typer, a CLI argument is added by simply adding arguments to the corresponding Python function:

```python
def main(name: str, last_name: str):
    print(f"Hello {name} {last_name}")

if __name__ == "__main__":
    typer.run(main())
```

### CLI Options

CLI options are CLI parameters passed to the CLI application with a specific name, for example:

```bash
# size is a CLI option
ls . --size
```

Typically, CLI options are optional, and their order is not important, that is, you can do:

```bash
# size is a CLI option
ls ./my-dir --size

ls --size ./my-dir
```

and obtain the same results.

CLI options can be added as shown below:

```python
def main(name: str, last_name: str, formal: bool = False):
  if formal:
    print(f"Good day, Ms. {name} {lastname}")
  else:
    print(f"Hey, {name} {lastname}")

if __name__ == "__main__":
  typer.run(main)
```

That will create two arguments `name` and `last_name` and one boolean option `--formal/--no-formal`.

### Converting a CLI argument into a CLI option

This just requires giving a value to the argument:

```python
def greeting(name: str, *, last_name: str = "", formal: bool = False) -> None:
    """Print a personalized greeting message."""
    if formal:
        print(f"Good day Ms. {name} {last_name}.!")
    else:
        print(f"Hey, Ms. {name} {last_name}!")
```

### Documenting your CLI app

The docstring attached to the function will be used in the CLI app help:

```python
def greeting(name: str, *, last_name: str = "", formal: bool = False) -> None:
    """
    Print a personalized greeting to NAME, optionally with a --last-name.

    If --formal is used, the greeting is more formal.
    """
    if formal:
        print(f"Good day Ms. {name} {last_name}.!")
    else:
        print(f"Hey, Ms. {name} {last_name}!")
```

### Displaying information with Rich

[Rich](https://rich.readthedocs.io/) comes by default when you install typer, which lets you display information in a prettied way: