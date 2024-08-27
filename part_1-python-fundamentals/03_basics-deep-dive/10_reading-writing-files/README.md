# Setting up shop

This Jupyter notebook uses Python 3.12.x and `venv`.

The Python installations are managed by `pyenv` so I've done:

```bash
# Select Python 3.12 as the Python version
$ pyenv global 3.12

# Set up a new virtual env named .venv
$ python -m venv .venv --upgrade-deps

# Activate the recently created virtual environment
# (vscode will be smart enough to activate it in the terminal for you)
$ source .venv/bin/activate

# Install the deps
$ python -m pip install -r requirements.txt
```

Then you will need to select the recently created `.venv` environment as the Jupyter notebook kernel.