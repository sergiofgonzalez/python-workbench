# Bundling of CLI apps with setup tools

## Building notes

Initially, the directory may contain only `appscript.py` and `setup.py`.

Right afterwards you can do:

```bash
# Use Python different from Linux OS one
conda activate base

# Create the virtualenv
python -m venv .venv --upgrade-deps

# Switch to virtualenv's Python
conda deactivate
source .venv/bin/active

# Install the package and bundle it
python -m pip install --editable .
```

Right afterwards, your command will be available directly from the command line:

```bash
$ appscript
Hello, world!
```

The `pip install --editable .` command installs a Python package in **editable mode**. This means that the package is installed in a way that allows you to make changes to the package's source code and see the changes reflected immediately in your environment.

This is useful when you are developing a package and want to test it in your environment without having to reinstall it every time you make a change.

The `.` at the end of the command specifies that the package should be installed from the current directory.



