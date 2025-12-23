# 010: number to words script
> illustrates how to structure a script that takes a number and transforms it into the equivalent textual representation

## Solution

The interesting techniques in this program are:
+ creating command-line tools with argparse.
+ dealing with stdin redirection to read from stdin as the user types, or by passing a file via `< file`.
+ running the script as a tool using `./n2w params`.

### `argparse`

The script uses argparse with a positional argument `number`, which is optional.

It is specified using:

```python
parser.add_argument(
    "number",
    nargs="*",  # One or more numbers
    help="The number to convert to words.",
)
```

`nargs` make `number` a list.

The optional argument is `-t/--test`, which is configured as:

```python
parser.add_argument(
    "-t",
    "--test",
    dest="test_mode",
    action="store_true",
    default=False,
    help="Enable test mode: reads numbers from stdin instead of command line.",
)
```

This makes `test_mode = True` when either -t or --test is specified, and `False` if not specified.

Then, you need to invoke `parser.parse_args()` to get the arguments into the script.

### dealing with stdin redirection

To make your script read from stdin, you simply need to use `sys.stdin` and a method to read the contents, such as `read()`:

```python
values = sys.stdin.read().split()
```

### running the script from the command line

To run the script from the program line, as if it was an executable, you just need to add the shebang line at the beginning of your Python program:

```python
#!/usr/bin/env python3
"""n2w: number to words converter.
...
"""

import argparse
import sys

...
```

Note that it will be executed with your Python3 installation. As this script is very simple and doesn't require any extra libs, it'll be OK. For more complex scenarios, it's better to rely on `uv` capabilities to deal with specific Python and Python library management for command-line tools.

After that, you'll need to make the Python file executable:

```bash
chmod +x n2w.py
```

## Running the program

See [README.md](../README.md#010-script-that-transforms-a-number-to-words) for full details.

You can run the application in many different ways

```bash
# do nothing
$ uv run n2w.py

# show help
$ uv run n2w.py --help

# run with a single number
$ uv run n2w.py 1,010,123

# run with several numbers
$ uv run n2w.py 1 2 3

# run in test mode with user typing into stdin
$ uv run n2w.py --test
Namespace(number=[], test_mode=True)
Test mode enabled. Reading numbers from stdin...
1
2
3
14
1 = one
2 = two
3 = three
14 = fourtee

# run in test mode by passing a file
$ uv run n2w.py --test < n2w_test.txt

# run as a command line tool
$ ./n2w.py 32155
```

