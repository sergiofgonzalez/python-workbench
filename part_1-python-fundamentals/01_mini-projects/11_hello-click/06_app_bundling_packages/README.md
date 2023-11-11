# Hello CLI app as a package for large applications
> illustrates how to do the CLI app bundling for complex CLI applications that are written within packages.

## Bundling notes

First, set up the virtual env:

```bash
$ conda run -n base python -m venv .venv --upgrade-deps && source .venv/bin/activat
```

Then, type:

```bash
$ python -m pip install --editable .
```

## Usage notes

Once bundled, you just need to type:

```bash
$ hello sfg --count 5
Hello to sfg
Hello to sfg
Hello to sfg
Hello to sfg
Hello to sfg
```
