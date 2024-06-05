# Using Poetry for the Jupyter notebook kernel

The kernel for this chapter is based on Poetry. This facilitates the addition of dependencies (even editable) for the project.

The steps to create the kernel for the first time are the following:

Start by running `poetry init` with the following parameters:

```bash
poetry init \
  --name 10-simulating-force-fields-ipynb \
  --description "10 - Simulating force fields" \
  --author "Sergio F. Gonzalez <sergio.f.gonzalez@gmail.com>" \
  --python "^3.10"
```

Then you will be asked interactively to provide additional information for your `pyproject.toml`. You can type "[ENTER]" to accept the defaults and select "no" when asked to provide the runtime and development dependencies.

After that, you will need to edit your [`pyproject.toml`](pyproject.toml) to inform that you intend to use the project in a *"non-package mode"*, meaning that you intend to use [`pyproject.toml`](pyproject.toml) to track dependencies and establish a virtual environment for the notebook.

This is done adding the option `package-mode = false` in the `[tool.poetry]` section:

```toml
[tool.poetry]
name = "10-simulating-force-fields-ipynb"
version = "0.1.0"
description = "10 - Simulating force fields"
authors = ["Sergio F. Gonzalez <sergio.f.gonzalez@gmail.com>"]
license = "MIT"
readme = "README.md"
package-mode = false

[tool.poetry.dependencies]
...
```

Finally, you can start adding dependencies to your project. Because you will be using this [`pyproject.toml`](pyproject.toml) for a Jupiter notebook, you will need to start adding the dependency to the `ipykernel` package:

```bash
$ poetry add ipykernel
```

As mentioned above, you can also add *editable* dependencies if needed. The following example illustrates how to add an editable dependency to the `20_matplotlib-helpers` project:

```bash
# Must point to where pyproject.toml is found
poetry add --editable ../../02_mini-projects/20_matplotlib-helpers/
```

At this point you can go ahead and create your Jupyter notebook, for example:

```bash
touch 10_simulating-force-fields/10_simulating-force-fields.ipynb
```

With all the dependencies in place and the notebook created, the only remaining step is to go to your Jupyter notebook and choose the kernel represented by your [`pyproject.toml`](pyproject.toml). This might require reopening the folder in which both your notebook and [`pyproject.toml`](pyproject.toml) are placed.



Note that those steps are only required for the first time setup. After having gone through those it is only required to recreate the environment by typing:

```bash
poetry install
```

and selecting the corresponding kernel in your notebook.