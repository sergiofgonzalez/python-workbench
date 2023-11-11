# toint
> practicing custom types

## Description

This simple CLI tool accepts an integer argument NUM that can be specified using hexadecimal or octal notation.

## Bundling

Create a virtual environment and then run:

```bash
python -m pip install --editable .
```

## Usage notes

Once bundled, you can do:

```bash
# using an int returns the same value
toint 5
5

# using a hex returns the base-10 integer value
toint 0xFE
254

# using an octal returns the base-10 integer value
toint 010
8
```