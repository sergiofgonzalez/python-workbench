# Typer examples

## Setting up shop

The project was created with:

```bash
uv init 01_typer-samples

uv add typer
```

## Running some examples

### Hello CLI with Typer

```bash
$ uv run typer 01_hello-cli-with-typer.py run
```

```bash
$ typer 01_hello-cli-with-typer.py run --help

 Usage: typer [PATH_OR_MODULE] run [OPTIONS] NAME

 Print a personalized greeting.

╭─ Arguments ──────────────────────────────────────────────────────────────╮
│ *    name      TEXT  [default: None] [required]                          │
╰──────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                              │
╰──────────────────────────────────────────────────────────────────────────╯
```

### 02: Using `typer` in your code

Assyming you've activated your virtual environment using `source .venv/bin/activate`

```bash
$ python 02_using-typer.py --help
```

```bash
$ python 02_using-typer.py "Jason Isaacs"
```

### 03: a more complex CLI app with subcommands

```bash
# show help for the app
$ python 03_using-subcommands.py goodbye --help

# show help for the particular command
$ python 03_using-subcommands.py goodbye --help
```

```bash
$ python 03_using-subcommands.py goodbye "Jason Isaacs"
Bye Jason Isaacs

$ python 03_using-subcommands.py goodbye --formal "Jason Isaacs"
Goodbye Ms. Jason Isaacs. Have a good day.
```

### 04: Converting an arg into an option

```bash
$ python 04_arg-into-option.py jason --formal --last-name isaacs
Good day Ms. jason isaacs.!
```