# Pip: editable install demo
> illustrates what a editable install means when running `pip install`


## Setting up shop

To set up the virtual environment run:

```bash
$ conda run -n base python -m venv .venv --upgrade-deps
$ source .venv/bin/activate
```

## Install `piplib` package using regular mode

This is the mode recommended for CI systems in production. It mimics what happens when you install a package from PyPI but using a project that is available in your file system.

For example, when using it with `11_piplib`

```bash
$ python -m pip install ../11_piplib
Processing /home/ubuntu/[...]/11_piplib
  Installing build dependencies ... done
  Getting requirements to build wheel ... done
  Preparing metadata (pyproject.toml) ... done
Building wheels for collected packages: piplib
  Building wheel for piplib (pyproject.toml) ... done
  Created wheel for piplib: filename=piplib-0.1.0-py3-none-any.whl size=1671 sha256=18c99f0b1b2034905dea6d0aace632fe7189dc18b221ff3cab214b932e24a7b6
  Stored in directory: /tmp/pip-ephem-wheel-cache-gbcbjjg_/wheels/f8/96/92/6afde033e6d8e154254505e984b271ca754f99b30e9381dc71
Successfully built piplib
Installing collected packages: piplib
Successfully installed piplib-0.1.0
```

Note that even if the build hasn't been performed in the package (`piplib`) it works by triggering that build in the corresponding installed package.

Also note that a change in the installed project won't be automatically available in the current project. Instead, you will be required to run `pip install` again.

## Install `piplib` package using editable mode

This is the recommended way to install packages available in your file system while developing both the package and the project.

The way to enable it is through the `-e` argument:

```bash
$ python -m pip install -e ../11_piplib
Obtaining file:///home/ubuntu/[...]/11_piplib
  Installing build dependencies ... done
  Checking if build backend supports build_editable ... done
  Getting requirements to build editable ... done
  Preparing editable metadata (pyproject.toml) ... done
Building wheels for collected packages: piplib
  Building editable for piplib (pyproject.toml) ... done
  Created wheel for piplib: filename=piplib-0.1.0-0.editable-py3-none-any.whl size=2735 sha256=3124607dacb82ca8c5f91875a202f08b6b004da84faab8662c0966a748eedaf6
  Stored in directory: /tmp/pip-ephem-wheel-cache-xobb11r1/wheels/f8/96/92/6afde033e6d8e154254505e984b271ca754f99b30e9381dc71
Successfully built piplib
Installing collected packages: piplib
Successfully installed piplib-0.1.0
```

The command also triggers a lightweight build on thee package library, but instead of copying the distribution, it only links to the files available there.

As a consequence, you will see your changes reflected, as long as there is no version change.

This even applies to changes in the exposed functions, or changes in the project metadata!
