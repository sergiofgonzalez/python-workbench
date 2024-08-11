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