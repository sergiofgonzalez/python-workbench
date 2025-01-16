# Hello, `mathproj`
> illustrating how to work with packages in Python

## Project setup

Project was built with `uv` using:

```bash
uv init 00_hello-mathproj
```

Then, the `hello.py` file was renamed to `main.py` (application entry point), and then the hierarchy of directories and files for `mathproj` was created as illustrated in the notebook.

The I ran:

```python
# create the virtual environment
uv venv
```

and adjusted the VS Code project virtual environment to the one recently created.

## main_v0.py

Loading the top-level module of the package. It illustrates that you can use the *symbols* defined in the top-level `__init__.py` and that importing the top-level package does not load the subpackages.