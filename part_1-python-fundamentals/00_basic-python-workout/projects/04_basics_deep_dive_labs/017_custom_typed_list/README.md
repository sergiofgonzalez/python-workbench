# Custom implementation of a TypedList
> hands-on implementation of a list that only accept elements of a given type

## Solution

The first interesting thing you should notice is that you can run the program using:

```bash
uv run custom-typed-list
```

while calling the module `typedlist` (that is, the code is within the `src/typedlist/` directory).

In order to do so, you have to make a few arrangements in your `pyproject.toml`:

```toml
[project]
name = "custom-typed-list"
...

[project.scripts]
custom-typed-list = "typedlist.main:main"

[tool.uv.build-backend]
module-name = "typedlist"
```

First, you can keep the `project.name` as `custom-typed-list`. The `project.name` is the distribution name, used when publishing to PyPI. You're not going to publish this package, but you want it to be `custom-typed-list` as it is more easily recognizable.

The `project.scripts` lets you define console entry points &mdash; command-line commands that get installed when your package is installed. The key `custom-typed-list` points to a function to run.

Finally, the `tool.uv.build-backend` is required because `uv_build` by default expects the package directory to match the normalized project name. Because of that, you need to explicitly tell `uv_build` where to find your package.



## Running the program

See [README.md](../README.md#017-using-duck-typing-to-create-a-typedlist) for full details.

Examples about how to run it.

You can run the application with:

```bash
uv run custom-typed-list
```
