# Managing projects
> a few notes about managing Python projects

## Using `venv` for Python projects
> distilled notes about using `venv`(note: `uv` is preferred, but `venv` is still used in many scenarios)

`venv` is the official module to create and manage separate virtual environments for your Python projects. It lacks certain capabilities other tools has like choosing a particular Python version, but it is still widely used and worth knowing.

### Creating and activating a new virtual environment

Follow these steps to create and activate a new virtual environment with `venv`:

```bash
# Create a new dir to host our Python project and cd into it
$ mkdir my-new-prj
$ cd my-new-prj

# Create the virtual environment (you need a valid Python runtime)
# Using the convention `.venv` as the virtual environnment name
$ python -m venv .venv

# Activate the newly created virtual environment
$ source .venv/bin/activate
(.venv) $

# Now we can install packages
(.venv) $ python -m pip install numpy
```

| NOTE: |
| :---- |
| Make sure to include your virtual environment name (e.g., `.venv`) in your `.gitignore`. |

### Deactivating a virtual environment

Once you're done with your virtual environment, you can do:

```bash
(.venv) $ deactivate
$
```

### Activating an existing virtual environment

You can reactivate an existing virtual environment typing:

```bash
$ source .venv/bin/activate
(.venv) $
```

### Upgrading the versions when creating a virtual environment

If you get a message informing you that `pip` is outdated when creating a virtual environment, you can use:

```bash
python -m venv .venv --upgrade-deps
```

### Additional information on virtual environments and `venv`

This has been a distilled list of venv related topics. More information is available on [02: Virtual Environments and Dependency Management](../../02_virtual_env_and_deps.ipynb).


## Using `uv` for Python projects
> distilled notes and opinionated recommendations for managing Python projects with `uv`

### Hello, uv!

[uv](https://github.com/astral-sh/uv) is a Python package and project manager written in Rust, which is intended to replace `pip`, `pix`, `poetry`, `pyenv`, `virtualenv`, and more.

You can find the documentation in their [docs](https://docs.astral.sh/uv).

### Installing uv

At the time of writing, the official installer is:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

That will install everything on `/home/$USER/.cargo/bin`

If everything goes well, you'll be able to type:

```bash
$ uv
An extremely fast Python package manager.

Usage: uv [OPTIONS] <COMMAND>

Commands:
...
```

No installation is finished without enabling shell autocompletion. In order to do so, run:

```bash
echo 'eval "$(uv generate-shell-completion bash)"' >> ~/.bashrc
```

### Upgrading uv

You can upgrade the version of an existing `uv` installation by typing:

```bash
$ uv self update
info: Checking for updates...
success: Upgraded uv from v0.8.3 to v0.9.15! https://github.com/astral-sh/uv/releases/tag/0.9.15
```

### Uninstalling uv

To cleanly remove `uv` and the data under `uv`'s control, run:

```bash
# clean uv cache
$ uv cache clean
$ rm -r "$(uv python dir)"
$ rm -r "$(uv tool dir)"
```

### Creating a project with `uv`

To create a Python project contained within a folder called example, type:

```bash
$ uv init example
```

To create a Python project with a specific Python version use:

```bash
$ uv init example --python 3.13
```


### Adding a new dependency to a project

To add a new package in an existing project, type:

```bash
uv add numpy
```

### Executing command line tools with `uv`

You can use `uvx` to execute and install command line tools contained in Python packages typing:

```bash
ux pycowsay "Hello to Jason Isaacs!"
```

### Managing tools with `uv`

You can use `uv` to make tools available user wide. For example, you can make `ruff` or `httpie` available by typing:

```bash
uv tool install httpie
```

You can upgrade the version of an installed typing:

```bash
uv toool upgrade ruff
```

You can type:

```bash
uv tool --help
```

to understand the different options available for tools (uninstall, list, etc.).

### Managing Python versions with `uv`

To install specific version of Python you can do:

```bash
uv python install 3.10 3.14
```

To create a virtual environment with a specific version of Python you can do:

```bash
uv venv --python 3.13.10
```

To upgrade an existing version you can do:

```bash
uv python upgrade 3.13
```

You can also update all installed Python versions doing:

```bash
uv python upgrade
```

### Managing scripts with uv

To run a script within the Python virtual environment created by `uv` type:

```bash
uv run <script>
```

For example, you can do:

```bash
$ python --version
Command 'python' not found, did you mean:
  command 'python3' from deb python3
  command 'python' from deb python-is-python3

$ uv run python --version
Python 3.14.1
```

Note that many times you might need to use `--` to treat arguments literally:

```bash
uv run -- flask run -p 3000
```

The equivalent manual actions of using `uv run` are:

```bash
# Make sure lockfile and virtual env are in sync
$ uv sync

# Activate the virtual environment
$ source .venv/bin/activate

# Run flask
$ flask run -p 3000
```


### Dependency management with `uv`

The following commands are the most popular ones:

```bash
# Add a dependency to the project
uv add numpy

# Specify a version constraint
$ uv add 'requests==2.31.0'

# Add a 'git' dependency
$ uv add requests --git https://github.com/psf/requests

# Add an 'editable' dependency
$ uv add --editable ../../../../../part_2-math/02_mini-projects/18-line-equations/

# Add a development only dependency
$ uv add --dev pytest

# Remove a dependency to the project
uv remove numpy

# Create a lockfile for the project's dependencies
uv lock

# Make sure lockfile and virtual env are in sync
$ uv sync

# View the dependency tree for the project
uv tree
```

### Misc utilities

The following commands can be used to manage and inspect `uv`'s state:


```bash
# Remove cache entries
$ uv cache clean

# Remove outdated cache entries
$ uv cache prune

# Show the uv cache directory path
$ uv cache dir

# Show uv's tool directory path
$ uv tool dir

# Show uv's installed Python versions path
$ uv python dir
```
