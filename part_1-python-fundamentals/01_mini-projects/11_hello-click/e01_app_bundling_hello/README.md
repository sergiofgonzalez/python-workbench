# Exercise: practicing CLI app bundling with setuptools

## Bundling notes

Once the virtualenv is setup run:

```bash
python -m pip install --editable .
```

## Usage notes

Once bundled, you can run your tool with:

```bash
$ hello "Jason Isaacs" --count 3
Hello to Jason Isaacs!
Hello to Jason Isaacs!
Hello to Jason Isaacs!
```