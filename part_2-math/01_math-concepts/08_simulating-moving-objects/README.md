# Using poetry

The kernel for the Jupyter notebook has been setup using Poetry.

The command to set that up was:

```bash
$ poetry init --name math-08-ipynb \
  --description "08 - Simulating moving objects" \
  --author "Sergio F. Gonzalez <sergio.f.gonzalez@gmail.com>" \
  --python "^3.10"
```

Then you need to add `package-mode = false` in the `[tool.poetry]` section, because you just need the dependencies and the virtual environment.

```python
[tool.poetry]
name = "math-08-ipynb"
version = "0.1.0"
description = "08 - Simulating moving objects"
authors = ["Sergio F. Gonzalez <sergio.f.gonzalez@gmail.com>"]
readme = "README.md"
package-mode = false
```

After that you need to add the dependencies, which must include the `ipykernel` package:

```bash
$ poetry add ipykernel
```

Note that you can also add *editable* dependencies:

```bash
# Must point to where pyproject.toml is found
poetry add --editable ../../02_mini-projects/20_matplotlib-helpers/
```