# Python tools

## [`pyenv`](https://github.com/pyenv/pyenv)

**pyenv** is a tool that lets you easily switch between multiple versions of Python (similar to *nvm* for the Node.js ecosystem). It lets you change the global Python vrsion on a per-user basis, and even provide support for a per-project Python versions.

The way in which `pyenv` determines the version to use is the following:

1. Searching for the `PYENV_VERSION` environment variable.

2. Looking for a `.python-version` file in the current directory. This can be created with the `pyenv local` command.

3. Looking for the first `.python-version` file found searching each parent directory, until reaching the root of your file system.

4. The global `$(pyenv root)/version` file. This can be modified using the `pyenv global` command.

| NOTE: |
| :---- |
| You can use `pyenv which <command>` to display which executable would be use to run a particular command. |

The pyenv-managed Python installations will be installed in the directories under `$(pyenv root)/versions`.

### Basic usage: Install, get versions and switch versions

To list versions available to install:

```bash
pyenv install -l
```

To install a specific version:

```bash
# Install specific version
pyenv install 3.12.2

# Install the latest 3.12
```

Check available versions

```bash
pyenv versions
```


Switch the global version to a specific one:

```bash
pyenv global 3.12
```

Verify the version has been correctly activated

```bash
python --version
```

| NOTE: |
| :---- |
| If you don't find a specific version, you might want to do `pyenv update`. |


## uv

[uv](https://github.com/astral-sh/uv) is a Python package and project manager written in Rust, which is intended to replace `pip`, `pix`, `poetry`, `pyenv`, `virtualenv`, and more.

You can find the documentation in their [docs](https://docs.astral.sh/uv).

The following section is a subset of that, focusing on the things I do more.

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
  run      Run a command or script
  init     Create a new project
  add      Add dependencies to the project
  remove   Remove dependencies from the project
  sync     Update the project's environment
  lock     Update the project's lockfile
  tree     Display the project's dependency tree
  tool     Run and install commands provided by Python packages
  python   Manage Python versions and installations
  pip      Manage Python packages with a pip-compatible interface
  venv     Create a virtual environment
  cache    Manage uv's cache
  self     Manage the uv executable
  version  Display uv's version
  help     Display documentation for a command
...
```

No installation is finished without enabling shell autocompletion. In order to do so, run:

```bash
echo 'eval "$(uv generate-shell-completion bash)"' >> ~/.bashrc
```

### Upgrading uv

When uv is installed, you can upgrade to the latest version by doing:

```bash
$ uv self update
info: Checking for updates...
success: You're on the latest version of uv (v0.3.5)
```

### Uninstalling uv

To cleanly remove uv and the data uv has stored before that, run:

```bash
# clean uv cache
$ uv cache clean
$ rm -r "$(uv python dir)"
$ rm -r "$(uv tool dir)"
```


### uv: Getting Started

#### First steps with uv

##### Project management

uv manages project dependencies and environments just like `poetry`:

```bash
# create a new project
$ uv init example

# cd into the newly created project
$ cd example

# add a new dependency
$ uv add pyenv
```

##### Tool management

uv can be used to execute and install command line tools provided by Python packages, just like `pipx` does:

```bash
uvx pycowsay "Hello to Jason Isaacs!"
```

You can also use this feature to make the tool available user wide, for example, to make `ruff` linter available from the command line, instead of as a per-project dependency:

```bash
# Install a tool user-wide
$ uv tool install ruff

# Now it's available from the command line
$ ruff --version
ruff 0.6.2
```

The tools will be installed in:

The tools will be managed by uv. See [Uninstalling uv](#uninstalling-uv) to understand how to manually remove tools.


##### Python Management

uv can install Python and allows for quickly switching between versions as `pyenv` does.

To install specific versions you can do:

```bash
uv python install 3.10 3.11 3.12
```

To create a particular virtual environment with a specific Python version you can do:

```bash
uv venv --python 3.12.5
```

#### Features

uv's interface is broken down into sections the provides the essential features for Python development.

##### Python versions

To install and manage Python.

```bash
# Install Python versions
uv python install

# View available Python versions
uv python list

# Find an installed Python version
uv python find

# Pin the current project to use a specific Python version
uv python pin

# Uninstall a Python version
uv python uninstall
```

| NOTE: |
| :---- |
| If you're managing Python versions with `pyenv` (as I was doing), you can install new versions with `uv`, but you won't be able to remove versions managed by `pyenv` with `uv`. |

##### Scripts

To execute standalone Python escripts

```bash
# Run a script
uv run

# Add a dependency to a script
uv add --script

# Remove a dependency from a script
uv remove --script
```

##### Projects

Creating and working on Python projects, with a `pyproject.toml`:

```bash
# Create a new Python project
uv init

# Add a dependency to the project
uv add

# Remove a dependency from the project
uv remove

# Sync the project's dependencies with the environment
uv sync

# Create a lockfile for the project's dependencies
uv lock

# Run a command in the project environment
uv run

# View the dependency tree for the project
uv tree
```

##### Tools

Running and installing tools published to Python package indexes such as ruff, black, etc.

```bash
# Run a tool in a temporary environment
uvx
uv tool run

# Install a tool user-wide
uv tool install

# Uninstall a tool
uv tool uninstall

# List installed tools
uv tool list

# Update the shell to include tool executables
uv tool update-shell
```

##### The pip interface

To manually manage environments and packages for legacy workflows, or for scenarios where the commands above do not provide enough control.

```bash
# Create a new virtual environment
uv venv
```

To manage packages in an environment:

```bash
#Install packages into the current environment
uv pip install

# Show details about an installed package
uv pip show

# List installed packages and their versions
uv pip freeze

# Check that the current environment has compatible packages
uv pip check

# List installed packages
uv pip list

# Uninstall packages
uv pip uninstall

# View the dependency tree for the environment
uv pip tree
```

Locking packages in an environment:

```bash
# Compile requirements into a lockfile
uv pip compile

# Sync an environment with a lockfile
uv pip sync
```

##### Utility

For managing and inspecting uv's state (cache, storage directories, self-updating, etc.)

```bash
# Remove cache entries
uv cache clean

# Remove outdated cache entries
uv cache prune

# Show the uv cache directory path
uv cache dir

# Show the uv tool directory path
uv tool dir

# Show the uv installed Python versions path
uv python dir

# Update uv to the latest version
uv self update
```

#### Getting help

To get help use:

```bash
# Get help for commands (short)
uv --help

# Get help for commands (long)
uv help

# Get help for a specific command (short)
uv init --help

# Get help for a specific command (long)
uv init help
```

### Guides

The following sections describe in detail the corresponding uv development workflows.

#### Installing Python
> https://docs.astral.sh/uv/guides/install-python

If Python is already installed on your system, uv will detect and use it.

However, you can install the latest Python version doing:

```bash
# install latest Python version
uv python install
```

To install a specific version:

```bash
uv python install 3.12
```

You can see the the available and installed Python versions for your system using:

```bash
$ uv python list
cpython-3.12.5-linux-x86_64-gnu     .pyenv/versions/3.12.5/bin/python3.12
cpython-3.12.5-linux-x86_64-gnu     .pyenv/versions/3.12.5/bin/python3 -> python3.12
cpython-3.12.5-linux-x86_64-gnu     .pyenv/versions/3.12.5/bin/python -> python3.12
cpython-3.12.5-linux-x86_64-gnu     <download available>
cpython-3.11.9-linux-x86_64-gnu     /usr/bin/python3.11
cpython-3.11.9-linux-x86_64-gnu     /bin/python3.11
cpython-3.11.9-linux-x86_64-gnu     <download available>
cpython-3.10.14-linux-x86_64-gnu    <download available>
cpython-3.9.19-linux-x86_64-gnu     <download available>
cpython-3.8.19-linux-x86_64-gnu     <download available>
cpython-3.8.10-linux-x86_64-gnu     /usr/bin/python3.8
cpython-3.8.10-linux-x86_64-gnu     /usr/bin/python3 -> python3.8
cpython-3.8.10-linux-x86_64-gnu     /usr/bin/python -> python3
cpython-3.8.10-linux-x86_64-gnu     /bin/python3.8
cpython-3.8.10-linux-x86_64-gnu     /bin/python3 -> python3.8
cpython-3.8.10-linux-x86_64-gnu     /bin/python -> python3
pypy-3.7.13-linux-x86_64-gnu        <download available>
```

#### Running scripts

A Python script is a file intended for standalone execution, typically doing:

```bash
$ python <script>.py
```

By using uv to run scripts, you ensure that script dependencies are managed without manually managing environments.

##### Running a script without dependencies

If your script has no dependencies, or depends on a module in the standard library (e.g., `sys`, `os`, `math`...) there's nothing extra to do &mdash; you can run it with `uv run`.

| NOTE: |
| :---- |
| We're assuming thatyou're running a script without a `pyproject.toml`. Otherwise, uv will first install the current project before running the script. |

uv will be able to run it even if no virtual environment is available.

| EXAMPLE: |
| :------- |
| You can try this with [wc](./mini-projects/00_wc-script/README.md). |

##### Running a script with dependencies

When the script requires other packages, they must be installed into the environment that the script runs in.

uv prefers to create these environments on-demand instead of using a long-lived virtual environment with manually managed dependencies.

It is recommended to specify the dependencies needed  using a `pyproject.toml` or using inline metadata:

```python
# /// script
# dependencies = [
#   "requests<3",
#   "rich",
# ]
# ///

import requests
from rich.pretty import pprint
...
```

but uv also supports passing the dependencies in the invocation with `--with` as in:

```bash
uv run --with rich 'requests<3'
```

Note that uv support the recent standard for specifying inline script metadata through a simple interface:

```bash
uv add --script <script>.py 'requests<3' 'rich'
```

To see that in action, consider the short programs I use to validate certain features I introduce into `vec2d` package. With uv I no longer need to maintain a project for this, I can have a single `vec2d_demo.py` script and do:

```bash
$ uv add --script vec2d_demo.py 'vec2d'
Updated `vec2d_demo.py`
```

This will change the script to look like the following:

```python
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "vec2d",
# ]
# ///
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "vec2d",
# ]
# ///
from vec2d.graph import (
    Arrow,
    Colors,
...
```

And then, I will be able to run it with:

```bash
uv run vec2d_demo.py
```

#### Using tools

Many Python packages provide apps that can be run as tools from the command line.

uv has specialized support for easily invoking and installing such tools.

To simply run a tool without installing it you can do:

```bash
# uvx is a shortcut for uv tool run
uvx ruff
```

Arguments can be provided too:

```bash
uvx pycowsay hello to jason isaacs
```

Sometimes, the package name and command is different, as it happens with `httpie` which provides the `http` command.

You can also use it with `uvx` by doing:

```bash
uvx --from httpie http
```

Obviously, you can also install tools to a persistent environment:

```bash
# install persistently, user-wide
$ uv tool install ruff

# now ruff is available
$ ruff --version
```

To upgrade a tool recently installed type:

```bash
uv tool upgrade ruff
```

You can also upgrade all tools by doing:

```bash
uv tool upgrade --all
```

You can list all the tools you have installed by doing:

```bash
$ uv tool list
ruff v0.6.2
- ruff
```

And you can do:

```bash
$ uv tool uninstall ruff
Uninstalled 1 executable: ruff
```

#### Working on projects

uv supports managing Python projects, which define their dependencies in a `pyproject.toml` file.

##### Creating a new project

To create a new project type:
```bash
$ pwd
/home/ubuntu/Development/git-repos/mini-projects

$ uv init hello-world

$ cd hello-world
```

Alternatively, you can also do:

```bash
$ mkdir hello-world

$ cd hello-world

$ uv init
```

this will create the following structure:

```
hello-world/
├── README.md
├── hello.py
└── pyproject.toml
```

As soon as you do:

```bash
$ uv run hello.py
Using Python 3.12.5 interpreter at: /home/ubuntu/.pyenv/versions/3.12.5/bin/python3
Creating virtualenv at: .venv
Hello from hello-world!
```

The virtual environment will be created, along with additional files and directories so that the final structure looks like the following:

```bash
hello-world/
├── .venv/
│   ├── bin/
│   ├── lib/
│   └── pyvenv.cfg
├── README.md
├── hello.py
├── pyproject.toml
└── uv.lock
```

+ The `pyproject.toml` contains metadata about your project. You can modify that file manually, or through commands such as `uv add` and `uv remove`.

    Specific configuration options for `uv` will be added in a `[tool.uv]` section.

+ The `.venv` folder will contain your project's virtual environment.

+ `uv.lock` is a cross-platform lockfile that contains the exact resolved versions that are installed in the project environment. This file **should** be checked into version control to enable consistent and reproducible installations across machines.

##### Adding and removing dependencies

You can add dependencies to your project's `pyproject.toml` with:

```bash
# Add `requests` package as a dependency to the project
$ uv add requests

# Specify a version constraint
$ uv add 'requests==2.31.0'

# Add a 'git' dependency
$ uv add requests --git https://github.com/psf/requests

# Add an 'editable' dependency
$ uv add --editable ../../../../../part_2-math/02_mini-projects/18-line-equations/
```

To remove a package you can do:

```bash
$ uv remove requests
```

##### Running commands

`uv run` can be used to run arbitrary scripts or commands in your project environment.

Prior to every `uv run` invocation, uv will verify that the lockfile is up-to-date with the `pyproject.toml`, and that the environment is up to date with the lockfile, making sure that the project is in-sync without any additional manual measures.

Thus, you can safely do:

```bash
$ uv add flask

# '--' is used to treat subsequent arguments literally
$ uv run -- flask run -p 3000
```

or to run a script:

```bash
uv run hello.py
```

The equivalent manual actions if you don't want to use `uv run` are:

```bash
# make sure lockfile and virtual env are in sync
$ uv sync

# activate the virtual environment
$ source .venv/bin/activate

# Run flask
$ flask run -p 3000

# Run hello.py
$ python hello.py
```

##### Publishing a package (https://docs.astral.sh/uv/guides/publish/)

