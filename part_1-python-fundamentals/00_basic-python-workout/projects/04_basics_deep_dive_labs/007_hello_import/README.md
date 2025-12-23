# 007: hello, import!
> basic usage of import

## Solution

In the example, you define a `mymath` module, but this time inside a directory with a `__init__.py`. You define the exported functions using `__all__`, which helps when you do `import mymath` by preventing importing things that should be kept inside the module.

## Running the program

See [README.md](../README.md#007-hello-import) for full details.

You can run the application with:

```bash
uv run main_import_1.py
uv run main_import_2.py
uv run main_import_3.py
```