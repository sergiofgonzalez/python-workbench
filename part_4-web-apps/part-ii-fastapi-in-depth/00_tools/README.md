# FastAPI related tools

This article discusses a few tools that work well with FastAPI.

## Poetry

While `pip` and `venv` are popular tools to do package and virtual environment management in Python, new tools have been created that combines them under a single tool. [Poetry](https://python-poetry.org/) is one of such packages.

Poetry manage dependencies in a `pyproject.toml` file.

### Installing Poetry

According to the installation documentation, Poetry should always be installed in a dedicated virtual environment, and never in the environment of the project that is to be managed by Poetry.

By doing so, you'll ensure that Poetry dependencies will not be accidentally upgraded or uninstalled.

The recommended way to install Poetry is with [`pipx`](https://github.com/pypa/pipx).

#### Installing `pipx`

[`pipx`](https://github.com/pypa/pipx) is a tool to install and run Python apps in isolated environments.

| NOTE: |
| :---- |
| `pipx` is similar to Node.js `npx`. |

To install [`pipx`](https://github.com/pypa/pipx) you need to follow the installation process for your operating system.

In my current OS, (Ubuntu 20.04), the commands are:

```bash
# Install and ensure path is ready to work with pipx
python3 -m pip install --user pipx
python3 -m pipx ensurepath
```

In order to upgrade `pipx`:

```bash
python3 -m pip install --user pipx --upgrade pipx
```

#### Proceeding with `poetry` installation

With `pipx` installed, you can proceed to install poetry:

```bash
$ pipx install poetry
  installed package poetry 1.7.1, installed using Python 3.8.10
  These apps are now globally available
    - poetry
done! ✨ 🌟 ✨
```

If you ever need to upgrade poetry, you can do so typing:

```bash
$ pipx upgrade poetry
poetry is already at latest version 1.7.1 (location: /home/ubuntu/.local/share/pipx/venvs/poetry)
```

And it can be deleted using:

```bash
$ pipx uninstall poetry
```

It's recommended to enable autocompletion for bash by typing:

```bash
poetry completions bash >> ~/.bash_completion
```

### Basic Usage

#### Project setup

To create a new project:

```bash
$ poetry new poetry-demo
Created package poetry_demo in poetry-demo
```

The created project will look like:

```
poetry-demo/
├── README.md
├── poetry_demo
│   └── __init__.py
├── pyproject.toml
└── tests
    └── __init__.py
```

| NOTE: |
| :---- |
| At this point you can rename the enclosing directory. |

The `pyproject.toml` file is the one that will orchestrate your project and its dependencies. It will initially look like:

```ini
[tool.poetry]
name = "poetry-demo"
version = "0.1.0"
description = ""
authors = ["Author <author@example.com>"]
readme = "README.md"

[tool.poetry.dependencies]
python = "^3.8"


[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
```

If you want to name your project differently than the folder you can type:

```bash
poetry new my-folder-name --name my-package-name
```

If you're a fan of `src/` folders to keep your source code, you can use:

```bash
poetry new --src my-package-name
```

which will create:

```
my-package-name/
├── pyproject.toml
├── README.md
├── src
│   └── my-package-name
│       └── __init__.py
└── tests
    └── __init__.py
```

The `--name` option can detect namespaces. As a result, you can do:

```bash
poetry new vec3d --name vec3d.graph
```

To create:

```bash
vec3d
├── README.md
├── pyproject.toml
├── tests
│   └── __init__.py
└── vec3d
    └── graph
        └── __init__.py
```

#### Initializing a pre-existing project

You can initialize a pre-existing project using `poetry init`. Note that this will guide you through the creation of the `pyproject.toml`, but won't help with the creation of the directory structure.

#### Specifying dependencies

You can specify dependencies manually by adding them in the `[tool.poetry.dependencies]` section, or you can use:

```bash
poetry add pendulum
```

When specifying dependencies you can use `^`, `~`, and `*` as you'd do in `NPM`. You can also use exact versions as in `requirements.txt` file.

+ `^` &mdash; allow SemVer compatible updates (as in `"^1.2.3"`, which allows to update between `>=1.2.3` and `<2.0.0`).
+ `~` &mdash; specify a minimal version with some ability to update. It's typically useful when you'd only want to update the patch section (as in `"~1.2.3"` which will update up to `"1.3.0"`, but not up to `"2.0.0"`, as `"^1.2.3"` would do).
+ `*` &mdash; allow for the update of the version where the wildcard is positioned.
+ `==` &mdash; to specify an exact version, as in `"==1.2.3"`. Note that Poetry also allows you to use `"1.2.3"` as well.


#### Using your virtual environment

By default, Poetry creates a virtual environment in `{[cache-dir](https://python-poetry.org/docs/configuration/#cache-dir)}/virtualenvs`.

By default, in Ubuntu `cache-dir` points to `~/.cache/pypoetry`.

It is also possible to use `virtualenvs.in-project` configuration variable to create the virtual environment in a directory named `.venv` within your project.

##### Using `poetry run`

To run a script (or Python command) under Poetry supervision simply type:

```bash
$ poetry run python main.py
Hello, world!

$ poetry run python --version
Python 3.8.10
```

| NOTE: |
| :---- |
| Unfortunately, Poetry will use the system's Python version, even if the `poetry new` command was issued with a different version. See [Managing environments](#managing-environments) below for workarounds and alternative approaches. |


Note that you can define scripts within your `pyproject.toml` and run them in the project's virtualenv with `poetry run`.

For example, if you update your `pyproject.toml`:

```ini
[tool.poetry.scripts]
my-script = "my-module:main"
```

you can then do:

```bash
poetry run my-script
```

This can be useful to accommodate dev tasks such as linting with pylint, checking types with mypy, etc.


##### Activating the virtual environment

The easiest way to activate and deactivate the virtual environment is to run:

```bash
# Creates a nested shell and activates the virtual env
$ poetry shell
 poetry shell
Spawning shell within /home/ubuntu/.cache/pypoetry/virtualenvs/poetry-demo-sMMG67ME-py3.8
. /home/ubuntu/.cache/pypoetry/virtualenvs/poetry-demo-sMMG67ME-py3.8/bin/activate

# exit the nested shell
$ exit
```

Alternatively, you can manually activate the virtual environment in the usual way running `source {path-to-env}/bin/activate`.

| NOTE: |
| :---- |
| To get the path to the current virtual environment type `poetry env info --path`. |

#### Installing dependencies

To install the dependencies for your project simply run:

```bash
poetry install
```

If there is a `poetry.lock` file present, Poetry will honor that lock file (meaning the exact versions found in the lock file will be downloaded if not available).

If there is no `poetry.lock` file, Poetry will resolve all the dependencies listed in `pyproject.toml` and download the latest version of their files. Once finished downloading, `poetry.lock` will be created with the specific downloaded versions.

The recommendations around `poetry.lock` file are:

+ As an application developer:

     You should commit `poetry.lock` to get reproducible builds. Using `pip install -e` will not honor the lock file.

+ As a library developer:

    Library developers have more things to consider, as the library will run in an environment the library developer do not control.

    You might consider leaving `poetry.lock` out of your version control, at the cost of losing reproducibility in your library.

    Alternatively, you might consider regular updates of the `poetry.lock` file to stay up-to-date with your dependencies.


When using `poetry install` the project is installed in editable mode by default.

That is:
+ `poetry install` &mdash; installs the project itself and its dependencies. This is the default.

+ `poetry install --no-root` &mdash; installs only the project's dependencies. The project itself remains in development mode. This can be useful in CI as you may want to install the dependencies for a project without installing the project which can save time and disk storage.

##### More on regular vs. editable installs

When dealing with local project install, that is, projects available in a directory in your computer, PIP distinguishes:

+ Regular installs &mdash; installs the project into the Python that pip is associated it, in a manner similar to how it would be actually installed if available in PyPI.

    ```bash
    python -m pip install path/to/SomeProject
    ```

    This is what should be used in CI systems for deployment. When using this mode, any change in `SomeProject` will require you to run `pip install` again.

+ Editable installs &mdash; installs a project without copying any files. Instead, the files in the development directory are added to Python's import path.

    ```bash
    python -m pip install -e path/to/SomeProject
    ```

    This is what should be used for development. When using this mode, changes in `SomeProject` will become immediately available without having to run `pip install -e` again.


| EXAMPLE: |
| :------- |
| See [pip-editable-demo](./10_pip-editable-demo/README.md) and [11_piplib](./11_piplib/README.md) for a runnable example the illustrate the differences between the two types of installs. Note that none of those projects use Poetry. |

You can use poetry in a similar fashion:

```bash
# Add using the regular local install
poetry add path/to/SomeProject

# Add using the editable mode
poetry add --editable path/to/SomeProject
```

#### Updating dependencies to their latest versions

Running `poetry install` when `poetry.lock` is present will prevent getting the latests versions of your dependencies as instructed on the `pyproject.toml`.

To update your dependencies, run:

```bash
poetry update
```

| NOTE: |
| :---- |
| `poetry update` is equivalent to deleting `poetry.lock` and then running `poetry install`. |

### Managing dependencies

#### Dependency groups

Poetry provides a way to organize your dependencies in *logical groups*.

This is useful to classify your dependencies as *test dependencies* or *dev dependencies*.

In order to add a group in your `pyproject.toml` you just need to add a section `tool.poetry.group.<group>.dependencies`.

For example:

```ini
[tool.poetry.dependencies]
python = "^3.8"
pendulum = "3.0.0"

[tool.poetry.group.test.dependencies]
pytest = "^6.0.0"
pytest-mock = "*"
```

The dependencies declared in `tool.poetry.dependencies` are part of an implicit `main` group.

Dependency groups, other than the implicit `main` group must only contain *dev-only* development tooling, as installing them will only be available using Poetry.

The proper way to declare dev depencies is using the group `dev`:

```ini
[tool.poetry.dependencies]
python = "^3.8"
pendulum = "3.0.0"

[tool.poetry.group.dev] # optional

[tool.poetry.group.dev.dependencies]
pytest = "^6.0.0"
pytest-mock = "*"
```

| NOTE: |
| :---- |
| All dependency groups must be consistent with each other. |

##### Optional groups

A dependency group can be declared as optional. This can be useful when you only require certain depencies in a particular environment of for a specific purpose:

```ini
[tool.poetry.dependencies]
python = "^3.8"
pendulum = "3.0.0"

[tool.poetry.group.docs]
optional = true

[tool.poetry.group.docs.dependencies]
mkdocs = "*"
```

You can install optional dependencies on top of the default dependencies using:

```bash
poetry install --with docs
```

##### Adding dependencies to a group

To add a dependency to a group type:

```bash
poetry add pytest --group test
```

That will automatically create the corresponding section in the `pyproject.toml` (if it doesn't exist) and add the corresponding dependency.

##### Installing group dependencies

By default, dependencies across all non-optional groups will be installed when executing `poetry install`.

If you want to exclude one or more groups, type:

```bash
poetry install --without test,docs
```

`--without` is useful in CI.

It is also possible to install a particular group by typing:

```bash
# Install only the dependencies found in docs section
poetry install --only docs

# Install only the dependencies found in main section
poetry install --only main
```

Finally, it is possible to run:

```bash
poetry install --only-root
```

This might be useful in scenarios in which you're only working on your project's core code and do not need the dependencies. It might also be useful when creating a distributable package, as you might want to ensure that only the essential components are included in the package.

##### Removing dependencies from a group

You can remove dependencies from a group using:

```bash
poetry remove mkdocs --group docs
```

#### Synchronizing dependencies

Synchronizing dependencies ensure that the locked dependencies found in `poetry.lock` are the only ones present in the environment:

```bash
poetry install --sync
```

That command can be combined dependency groups to include or exclude specific groups:

```bash
poetry install --without dev --sync
poetry install --with docs --sync
```

#### Layering optional groups

Omitting the `--sync` option lets you install any subset of optional groups, which might be useful when creating multi-stage Docker builds.

### Libraries

This section illustrates how to make your library installable through Poetry.

#### Versioning

Poetry requires projects compliant with [PEP 440](https://peps.python.org/pep-0440).

As a result, you shoud use `1.0.0-hotfix1` or `1.0.0.hotfix1` (instead of `1.0.0-hotfix.1`).

#### Lock file

For your library, you may commit `poetry.lock` but you should take into account that the lock file will have no effect on other projects that depend on it &mdash; it only has effect on the main project.

Committing the file might help your library development team, as they will have reproducible builds.

#### Packaging

You can package a project by typing:

```bash
poetry build
```

Packaging a project is a prerequisite to actually publishing it.

#### Publishing to PyPI

Once the package has been built you can type:

```bash
poetry publish
```

This will publish the package in PyPI by default.

| NOTE: |
| :---- |
| `publish` will require you to have your credentials configured. See [Configuring Credentials](#configuring-credentials). |


By default, `publish` does not execute `build` by default. Howevery you can do:

```bash
poetry publish --build
```

#### Publishing to a private repository

To publish to a private repository you can do:

```bash
poetry publish -r my-repository
```

### Commands

Poetry supports a lot of commands. You can get help for any of the commands by using `--help`.

You can find the documentation in [Poetry commands](https://python-poetry.org/docs/cli/).

These are a few commands and options that hadn't been mentioned before.

#### `poetry config`

```bash
# list config parameters
poetry config --list

# list specific setting
poetry config virtualenvs.in-project

# Setting a specific key globally
poetry config virtualenvs.in-project true

# Setting a specific key local to this project only
# i.e., will be written to poetry.toml
poetry config virtualenvs.in-project true --local

# Unset a particular key
poetry config virtualenvs.in-project --unset
```

#### `poetry version`

This command shows the current version of the project or bumps the version of the project and writes the new version back to `pyproject.toml` if a valid bump rule is provided.

The following table illustrates the available rule options in poetry and their effect:

| Rule | Before | After |
| :--- | :----- | :---- |
| major | 1.3.0 | 2.0.0 |
| minor | 2.1.4 | 2.2.0 |
| patch | 4.1.1 | 4.1.2 |
| premajor | 1.0.2 | 2.0.0a0 |
| preminor | 1.0.2 | 1.1.0a0 |
| prepatch | 1.0.2 | 1.0.3a0 |
| prerelease | 1.0.2 | 1.0.3a0 |
| prerelease | 1.0.3a0 | 1.0.3a1 |
| prerelease | 1.0.3b0 | 1.0.3.b1 |
| prerelease --next-phase | 1.0.3a0 | 1.0.3b0 |
| prerelease --next-phase | 1.0.3b0 | 1.0.3rc0 |
| prerelease --next-phase | 1.0.3rc0 | 1.0.3 |

#### `poetry cache`

The `cache` command lets you interact with Poetry's cache:

```bash
# List available caches
$ poetry cache list
PyPI
_default_cache

# clear all packages from a cached repo
poetry cache clear pypi --all

# clear specific package from a cached repo
poetry cache clear pypi:requests:2.24.0
```

#### `poetry source`

The `source` command lets you manage repository sources for a Poetry project.

```bash
# Add pypi-test repo
poetry source add pypi-test https://test.pypi.org/simple/

# Set the priority of pypi (when using multiple)
poetry source add --priority=explicit pypi
```

### Configuration

Poetry global configuration is stored under `~/.config/pypoetry`.

However, you can provide project specific configuration using `--local` option, and then, it will be stored in `poetry.toml`.

| NOTE: |
| :---- |
| Be mindful of committing `poetry.toml`, as it may contain user-specific configuration. |

When dealing with CI, it's often preferable to use environment variables instead of running configuration commands.

Poetry supports setting any configuration key via environment variable by prefixing the environment variable by `POETRY_` and replacing any `.` and `-` by `_` as in:

```bash
export POETRY_VIRTUALENVS_IN_PROJECT=true
```

You can find the list of available settings [here](https://python-poetry.org/docs/configuration/#available-settings).

The directories used by Poetry are:

+ config &mdash; `~/.config/pypoetry`
+ cache &mdash; `~/.cache/pypoetry`
+ data directory &mdash; `~/.local/share/pypoetry`

### Repositories

By default, Poetry is configured to use PyPI repository for package installation and publishing. However, it supports also private repositories.


#### Installing from non-PyPI sources

When using non-pypi repositories, you first need to configure the package source.

```bash
poetry source add --priority=supplemental pypi-test https://test.pypi.org/simple/
```

Then, you will need to provide the credentials for it (if not a public repo):

```bash
# Using tokens
poetry config pypi-token.pypi-test <my-pypi-test-token>

# Alternatively: if using username and pass
poetry config http-basic.pypi-test <username> <pass>
```

Right afterwards, you will be able to add dependencies from that source:

```bash
poetry add --source pypi-test my-test-package
```

#### Publishing to non-PyPI repositories

The workflow is similar when you want to publish to a private repo.

First you need to configure the Upload API endpoint for your repo:

```bash
poetry config repositories.private-pypi https://pypi.example.com/legacy/
```

Then you'll need to configure your credentials:

```bash
poetry config http-basic.private-pypi <username> <pass>
```

And you'll be ready to publish:

```bash
poetry publish --build --repository private-pypi
```

#### More on Package sources

With the exception of PyPI source (named `pypi`), package source are local to a project and must be configured within the project's `pyproject.toml`. This only applies to installing packages &mdash; when publishing a package the situation is different.

Whenever you run a command such as:

```bash
poetry source add --priority=supplemental pypi-test https://test.pypi.org/simple/
```

A snippet will be added to your project's `pyproject.toml`:

```bash
[[tool.poetry.source]]
name = "pypi-test"
url = "https://test.pypi.org/simple/"
priority = "supplemental"
```

The `--priority` option classifies the repository as:

1. `default` &mdash; PyPI by default. You can alter this behavior by explicitly setting another default repository (e.g., `poetry source add --priority=default https://internal-pypi.example.com/simple/`).
2. `primary` &mdash; default value when omitted. A primary source will take precedence over PyPI and the rest of the categories.
3. PyPI, unless disabled explicitly.
4. `supplemental` &mdash; searched only if no other higher-priority source yields a compatible package distribution.
5. `explicit` &mdash; searched only when a package configuration explicitly indicates that it should be found on that source (e.g., `poetry add --source internal-pypi vec3d`).

If you want to disable PyPI completely, you can set your source as the default

#### Supported package sources

PyPI its supported using its JSON API. Poetry can fetch and install package dependencies from public or private repost that implement the simple repository API.

Those need to be configured as explaine above:

```bash
poetry source add pypi-test https://test.pypi.org/simple/
```

#### More on Publishable Repositories

Poetry treats repositories to which you publish packages as user specific and not project specific (unlike sources).

Additionally, Poetry only supports the Legacy Upload API when publishing projects and therefore, need to be configured with specific URLs:

```bash
poetry config repositories.testpypi https://test.pypi.org/legacy/
```

| NOTE: |
| :---- |
| The Legacy API is also used when publishing your package using `twine` as seen on the documentation [Python fundamentals: Package Publishing](../../../part_1-python-fundamentals/00_basic-python-workout/04_package_publishing.ipynb). |

### Managing environments

Poetry will always work isolated from your global Python installation. To achieve this, it will first check if it's currently running side a virtual environment. If it is, it will use it directly, and if it's not, it will either use one that has already created or create a brand new one for you.

By default, Poetry will try to use the Python version used during Poetry's installation to create the virtual environment for the current project.

In my system, I use miniconda to handle the different Python versions. A possible way to fine tune the Python version used by Poetry to set up the environment (so that is not the default Ubuntu 20.04 Python 3.8.* version) is to set the experimental `virtualenvs.prefer-active-python` to `true` which will make Poetry try to find the current `python` of your shell.

```bash
poetry config virtualenvs.prefer-active-python true
```

With that option enabled, you can do:

```bash
# Create a new project using a non-default python (3.10)
$ conda run -n web \
poetry new 50-conda-poetry-demo --name poetry-demo

# pyproject.toml uses now ^3.10
$ cd 50-conda-poetry-demo
$ cat $ cat pyproject.toml
...

[tool.poetry.dependencies]
python = "^3.10"

...
```

However, when doing:

```bash
$ poetry run python --version
The currently activated Python version 3.8.10 is not supported by the project (^3.10).
Trying to find and use a compatible version.
...
```

Which means that does not solve the problem in its entirety.

#### Enter `pyenv`

pyenv is tool that lets you easily switch between multiple versions of Python.

`pyenv` lets you change the global Python version on a per-user basis and even provide support for per-project Python versions.

`pyenv` determines which Python version to use by trying the following sources in order:

1. `PYENV_VERSION` environment variable (if specified). You can use `pyenv shell` to set this environment variable in your current shell session.

2. A `.python-version` file in the current directory, which can be created with the `pyenv local` command.

3. The first `python-version` file found searching each parent directory, until reaching the root of your file system.

4. The global `$(pyenv root)/version` file that can modified using the `pyenv global` command. If no such file is present, `pyenv` assumes you want to use the "system" Python.

Note that you can use `pyenv which <command>` to display which executable would be use to run a particular command.

The installed Pyenv-managed Python installations will be installed in directories under `$(pyenv root)/versions`.

##### Installation and update
> See https://github.com/pyenv/pyenv?tab=readme-ov-file#installation for the latest information


pyenv can be installed using:

```bash
curl https://pyenv.run | bash
...
WARNING: seems you still have not added 'pyenv' to the load path.

# Load pyenv automatically by appending
# the following to
# ~/.bash_profile if it exists, otherwise ~/.profile (for login shells)
# and ~/.bashrc (for interactive shells) :

export PYENV_ROOT="$HOME/.pyenv"
[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"

# Restart your shell for the changes to take effect.

# Load pyenv-virtualenv automatically by adding
# the following to ~/.bashrc:

eval "$(pyenv virtualenv-init -)"
```

The additional bash configuration details are:

1. Add the following lines to your `.bashrc` so that it affects the interactive shells:

    ```bash
    export PYENV_ROOT="$HOME/.pyenv"
    command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"
    eval "$(pyenv init -)"
    ```

2. Add the same lines to your `.profile` (as I don't have `~/.bash_profile` or `~/.bash_login`).

Then, before attempting to install a new Python version you need to install Python build dependencies.

```bash
sudo apt update; sudo apt install build-essential libssl-dev zlib1g-dev \
libbz2-dev libreadline-dev libsqlite3-dev curl \
libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev
```

##### Basic Usage: Install, get versions, and switch versions

To list versions available to install:

```bash
pyenv install -l
```

To install a specific Python version run `pyenv install`:

```bash
$ pyenv install 3.10.13
Downloading Python-3.10.13.tar.xz...
-> https://www.python.org/ftp/python/3.10.13/Python-3.10.13.tar.xz
Installing Python-3.10.13...
Installed Python-3.10.13 to /home/ubuntu/.pyenv/versions/3.10.13
```

| NOTE: |
| :---- |
| You can also do `pyenv install 3.10` and pyenv will pick the latest known version. |

Get the versions available to pyenv:

```bash
$ pyenv versions
* system (set by /home/ubuntu/.pyenv/version)
  3.10.13
```

Switch the global version to the latest 3.10 (by default global is system as seen above):

```bash
# This makes 3.10.* the preferred version to use
$ pyenv global 3.10

# Check available versions
$ pyenv versions
  system
* 3.10.13 (set by /home/ubuntu/.pyenv/version)

# Now Python 3.10.13 is the default version for the user account
$ python --version
Python 3.10.13
```

Now, whenever you invoke `python`, `pip`, etc., and executable from the provided 3.10.13 installation will be run instead of the system python.

##### Uninstalling a Python version

To uninstall a version type:

```bash
$ pyenv uninstall <version>
```

This has the effect of removing the directory in which Python was installed. That directory can be found using what is explained in the next section

##### Finding where a Python version has been installed

```bash
$ pyenv prefix 3.10.13
/home/ubuntu/.pyenv/versions/3.10.13
```

##### Obtaining help on commands and subcommands

Obtaining help:

```bash
pyenv <command> <subcommand> --help
```

##### Updating pyenv executable

To update pyenv to the latest version:

```bash
pyenv update
```

##### Disabling pyenv

To disable pyenv temporarily, you just need to remove the `pyenv init` invocation from your shell startup configuration.

##### Uninstalling pyenv

1. Remove all pyenv configuration lines from `~/.profile` and `~/.bashrc`.

2. Run `rm -rf $(pyenv root)`. This will remove all Python versions installed.

##### Additional information

For additional information on pyenv, please visit the official [Github page](https://github.com/pyenv/pyenv) for the project.

#### Back to Managing environments

With `pyenv` in place and the `virtualenvs.prefer-active-python` option set to `true`, you `poetry` will be able to create new projects with the desired Python version:

```bash
$ poetry new poetry-demo
Created package poetry_demo in poetry-demo

$ cd poetry-demo
cat pyproject.toml
...

[tool.poetry.dependencies]
python = "^3.10"

...

$ poetry run python --version
$ poetry run python --version
Creating virtualenv poetry-demo-OI2glpu1-py3.10 in /home/ubuntu/.cache/pypoetry/virtualenvs
Python 3.10.13
```

Note that with this approach and leveraging on `pyenv`'s ability to use different python versions per directory you will be able to create specific projects with the desired version:

```bash
# Create a new dir for Python 3.11.* projects and cd into it
$ mkdir python-3.11-projects
$ cd python-3.11-projects

# Install Python 3.11 with pyenv
$ pyenv install 3.11
Downloading Python-3.11.7.tar.xz...
-> https://www.python.org/ftp/python/3.11.7/Python-3.11.7.tar.xz
Installing Python-3.11.7...
Installed Python-3.11.7 to /home/ubuntu/.pyenv/versions/3.11.7

# Make Python 3.11 the default for projects in the directory
$ pyenv local 3.11

$ cat .python-version
3.11

# It works!
$ python --version
Python 3.11.7

# Create a new project with poetry
$ poetry new poetry-demo

$ cat poetry-demo/pyproject.toml
...

[tool.poetry.dependencies]
python = "^3.11"

...

$ poetry run python --version
Creating virtualenv poetry-demo-U5Sau-cw-py3.11 in /home/ubuntu/.cache/pypoetry/virtualenvs
Python 3.11.7
```

| NOTE: |
| :---- |
| Alternatively, you can use something like `poetry env use /full/path/to/python`. |


#### Displaying the environment information

To get the basic information about the currently activated virtual environment you can use:

```bash
# Running it on a pyenv-managed Python 3.11 directory
$ poetry env info

Virtualenv
Python:         3.11.7
Implementation: CPython
Path:           /home/ubuntu/.cache/pypoetry/virtualenvs/poetry-demo-U5Sau-cw-py3.11
Executable:     /home/ubuntu/.cache/pypoetry/virtualenvs/poetry-demo-U5Sau-cw-py3.11/bin/python
Valid:          True

System
Platform:   linux
OS:         posix
Python:     3.11.7
Path:       /home/ubuntu/.pyenv/versions/3.11.7
Executable: /home/ubuntu/.pyenv/versions/3.11.7/bin/python3.11

# Running it on a global Python 3.10 project directory
$ poetry env info

Virtualenv
Python:         3.10.13
Implementation: CPython
Path:           /home/ubuntu/.cache/pypoetry/virtualenvs/poetry-demo-OI2glpu1-py3.10
Executable:     /home/ubuntu/.cache/pypoetry/virtualenvs/poetry-demo-OI2glpu1-py3.10/bin/python
Valid:          True

System
Platform:   linux
OS:         posix
Python:     3.10.13
Path:       /home/ubuntu/.pyenv/versions/3.10.13
Executable: /home/ubuntu/.pyenv/versions/3.10.13/bin/python3.10

# Running it on a directory right after running poetry new
$ poetry env info

Virtualenv
Python:         3.8.10
Implementation: CPython
Path:           NA
Executable:     NA

System
Platform:   linux
OS:         posix
Python:     3.8.10
Path:       /home/ubuntu/.local/share/pipx/venvs/poetry
Executable: /home/ubuntu/.local/share/pipx/venvs/poetry/bin/python3

# Running it on the same dir after having run poetry commands
$ poetry env info

Virtualenv
Python:         3.10.13
Implementation: CPython
Path:           /home/ubuntu/.cache/pypoetry/virtualenvs/some-project-gHBV0K9r-py3.10
Executable:     /home/ubuntu/.cache/pypoetry/virtualenvs/some-project-gHBV0K9r-py3.10/bin/python
Valid:          True

System
Platform:   linux
OS:         posix
Python:     3.10.13
Path:       /home/ubuntu/.pyenv/versions/3.10.13
Executable: /home/ubuntu/.pyenv/versions/3.10.13/bin/python3.10

# Running it outside a Poetry directory
$ poetry env info

Poetry could not find a pyproject.toml file in /home/ubuntu/ or its parents
```

#### Listing the environments associated with the project

Run:

```bash
$ poetry env list
poetry-demo-OI2glpu1-py3.10 (Activated)
```

#### Deleting the environments

You can delete existing virtual environments using `poetry env remove`:

```bash
$ poetry env list --full-path
/home/ubuntu/.cache/pypoetry/virtualenvs/poetry-demo-OI2glpu1-py3.10 (Activated)

$ poetry env remove poetry-demo-OI2glpu1-py3.10
Deleted virtualenv: /home/ubuntu/.cache/pypoetry/virtualenvs/poetry-demo-OI2glpu1-py3.10
```

You can also type the following to remove all virtual environments associated to the current project.

```bash
$ poetry env remove --all
```

### Publishing an existing `setup.py` project using Poetry

This section illustrates the specific steps you need to follow and commands you need to type to publish an existing Python package that was using the `setup.py` approach using Poetry.

The example uses the `vec3d` project, whose version `v0.2.3` used `setup.py`. The goal is to publish `v0.2.4` using Poetry.

1. Create a new poetry based project.

        In this first step you use `poetry new` to create a new poetry-based project. This will create the initial structure for us, that we will then move to the existing project.

        ```bash
        poetry new vec3d-poetry --name vec3d.graph
        ```

        Because `--name` supports a single argument, you simply need to use one of the subpackages the module has (in any case, no sources will be modified).

2. Manually transport the `setup.py` information to `pyproject.toml`.

        Both files contain roughly the same information, so you just need to adjust the syntax.

        The original `setup.py´ file was:

        ```python
        from setuptools import setup

        with open("README.md", encoding="utf-8") as file:
            read_me_description = file.read()

        setup(
            name="vec3d",
            version="0.2.3",
            author="Sergio F. Gonzalez",
            author_email="sergio.f.gonzalez@gmail.com",
            description="Maths and graph functions for vectors in the 3D space",
            long_description=read_me_description,
            long_description_content_type="text/markdown",
            url="https://github.com/sergiofgonzalez/vec3d",
            packages=["vec3d/graph", "vec3d/math"],
            include_package_data=True,
            install_requires=["matplotlib", "numpy"],
            classifiers=[
                "Programming Language :: Python :: 3",
                "License :: OSI Approved :: MIT License",
                "Operating System :: OS Independent",
            ],
            python_requires=">=3.10",
        )
        ```

        The equivalent `pyproject.toml` will be:

        ```toml
        [tool.poetry]
        name = "vec3d"
        version = "0.1.0"
        description = "Maths and graph functions for vectors in the 3D space"
        authors = ["Sergio F. Gonzalez <sergio.f.gonzalez@gmail.com>"]
        readme = "README.md"
        license = "MIT"
        repository = "https://github.com/sergiofgonzalez/vec3d"
        packages = [{include = "vec3d"}]

        [tool.poetry.dependencies]
        python = "^3.10"


        [build-system]
        requires = ["poetry-core"]
        build-backend = "poetry.core.masonry.api"
        ```

        That is, you only need to populate the description, state the license and the repository.

        The version field also needs to be copied.

        Note that Poetry is smart enough to autodiscover the subpackages, and therefore, you don't need to explicitly include `vec3d.graph` and `vec3d.math` you have in `setup.py`.


3. Copy the `pyproject.toml` to the `vec3d/` local repo.

        After this point, you can remove the `poetry-vec3d` project.

4. Add the project dependencies.

        Now you can use `poetry add` to include the project's dependencies.

        ```bash
        poetry add matplotlib numpy
        ```

        Additionally, you can also include pylint as a dev dependency:

        ```bash
        poetry add pylint --group dev
        ```


4. Remove the old setup-related artifacts.

        Now you can remove `setup.py`, `requirements.txt` and run `make clean` to get rid of the existing distribuition and build artifacts.

        Right afterwards, you can get rid of the `Makefile` too.

        Up until now, the project was also using the pre-existing virtual environment. We want Poetry to manage this too, so we can get rid of `.venv/` too. Running a `poetry run` command will be sufficient to trigger the creation of a new virtual env for our project.

        ```bash
        $ rm -rf .venv

        $ poetry run python --version
        Creating virtualenv vec3d-k7MeA7C0-py3.10 in /home/ubuntu/.cache/pypoetry/virtualenvs
        Python 3.10.13
        ```

        Now, you need to run `poetry install` to ensure the new virtual environment contains the necessary dependencies.

        You can ensure everything is correctly wired by running:

        ```bash
        $ poetry run pylint vec3d/

        ------------------------------------
        Your code has been rated at 10.00/10
        ```

        And also:

        ```bash
        $ poetry run python -m unittest discover
        ........
        ----------------------------------------------------------------------
        Ran 8 tests in 0.001s

        OK
        ```

5. Publishing to Test PyPI.

        With the project working in local you're almost ready to publish to Test PyPI.

        Poetry helps with the version management via the `poetry version` command.

        Before publishing to Test PyPI, you run the following command to announce that you are in the pre-release phase. It it is recommended to use `--dry-run` first to check you're getting the intended version bump.

        ```bash
        $ poetry version prerelease --dry-run
        Bumping version from 0.2.3 to 0.2.4a0

        # yup, that's what I want
        $ poetry version prerelease
        ```

        Before publishing, you need to configure the Test PyPI repo, as Poetry is configured with PyPI only:

        ```bash
        # Configure "testpypi" repo using Legacy Upload API
        $ poetry config repositories.testpypi https://test.pypi.org/legacy/

        # Configure the credentials to publish in that repo
        poetry config pypi-token.testpypi pypi-Ag...5yn
        ```

        Now you can publish in a single command:

        ```bash
        poetry publish --build -r testpypi
        Building vec3d (0.2.4a0)
        - Building sdist
        - Built vec3d-0.2.4a0.tar.gz
        - Building wheel
        - Built vec3d-0.2.4a0-py3-none-any.whl

        Publishing vec3d (0.2.4a0) to testpypi
          - Uploading vec3d-0.2.4a0-py3-none-any.whl 100%
          - Uploading vec3d-0.2.4a0.tar.gz 100%
        ```

        Note that publishing repositories are not defined per-project. As a result, you won't need to configure testpypi repository or credentials anymore.

5. Validating the published artifact in TestPyPI.

        Now you can https://test.pypi.org/project/vec3d and validate that the page contains look as they were when using the `setup.py`.

6. Validating the library in a program.

        With the library published, you can create a small program to validate that it works as intended.

        The first thing you can do is advance the release phase up to the release candidate:

        ```bash
        $ poetry version prerelease --next-phase
        Bumping version from 0.2.4a0 to 0.2.4b0

        $ poetry version prerelease --next-phase
        Bumping version from 0.2.4b0 to 0.2.4rc0
        ```

        Then, you can republish:

        ```bash
        $ poetry publish --build -r testpypi
        Building vec3d (0.2.4rc0)
        - Building sdist
        - Built vec3d-0.2.4rc0.tar.gz
        - Building wheel
        - Built vec3d-0.2.4rc0-py3-none-any.whl

        Publishing vec3d (0.2.4rc0) to testpypi
          - Uploading vec3d-0.2.4rc0-py3-none-any.whl 100%
          - Uploading vec3d-0.2.4rc0.tar.gz 100%
        ```

        Now, you can create a simple project that uses `vec3d@0.2.4rc0` from Test PyPI and validate that it works as expected.

        Poetry will also simplify this task:

        ```bash
        $ poetry new vec3d-demo
        ```

        Note that repositories that you consume are configured on a per-project basis. That it, you will need to define a source for Test PyPI assign the repo a priority, and then add the depedency from that repo:

        ```bash
        $ poetry source add --priority=explicit testpypi https://test.pypi.org/simple/

        $ poetry add vec3d==0.2.4rc0 --source testpypi
        ```

        Note that the first command will have modified the demo project `pyproject.toml` to include the following:

        ```ini
        [[tool.poetry.source]]
        name = "testpypi"
        url = "https://test.pypi.org/simple/"
        priority = "explicit"
        ```

        Right after that you can program and test the demo using:

        ```bash
        poetry run python main.py
        ```

        If everything goes as expected you will be ready to publish to PyPI!

7. Publishing to PyPI.

        The first thing you need to do is bump up the version to final.

        ```bash
        $ poetry version prerelease --next-phase
        Bumping version from 0.2.4rc0 to 0.2.4
        ```

        Then you need to configure your credentials for PyPI. This time you don't need to configure the PyPI repo because that comes predefined in Poetry with the name `"pypi"`.

        ```bash
        poetry config pypi-token.pypi pypi-Ag...Dsw
        ```

        Right after that you can run the build+publish:

        ```bash
        poetry publish --build
        Building vec3d (0.2.4)
        - Building sdist
        - Built vec3d-0.2.4.tar.gz
        - Building wheel
        - Built vec3d-0.2.4-py3-none-any.whl

        Publishing vec3d (0.2.4) to PyPI
        - Uploading vec3d-0.2.4-py3-none-any.whl 100%
        - Uploading vec3d-0.2.4.tar.gz 100%
        ```

        At this point it is recommended to tag the repo.

8. Validating the library in a program.
