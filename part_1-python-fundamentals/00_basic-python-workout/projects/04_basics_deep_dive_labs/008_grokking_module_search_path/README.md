# 008: grokking Python's module search path
> deep dive on how Python's find the modules you import

## Solution

As explained in the exercise, the variable `sys.path` contains all the paths where Python will try to find modules.

Additionally, you know that `PYTHONPATH` environment variable can be used to include additional paths.

By default in my installation, `PYTHONPATH` is empty and the elements of `sys.path` are:

- /home/ubuntu/.../008_grokking_module_search_path
- /home/ubuntu/.local/share/uv/python/cpython-3.14.1-linux-x86_64-gnu/lib/python314.zip
- /home/ubuntu/.local/share/uv/python/cpython-3.14.1-linux-x86_64-gnu/lib/python3.14
- /home/ubuntu/.local/share/uv/python/cpython-3.14.1-linux-x86_64-gnu/lib/python3.14/lib-dynload
- /home/ubuntu/.../008_grokking_module_search_path/.venv/lib/python3.14/site-packages

Therefore, by default, if I want to consume via import a reusable module it has to be placed in one of those directories. However, it's only recommended to use /home/ubuntu/.../008_grokking_module_search_path because the other ones are site specific packages that are managed by the Python installation or the virtual environment.


You can alway configure the `PYTHONPATH` environment variable to include additional directories that will be used by Python to locate additional packages.

For example, if you do:

 ```bash
 $ PYTHONPATH="/home/ubuntu/Development/git-repos/side-projects/delete_me/" uv run main.py
 ```

The module search path elements will be updated to:
- /home/ubuntu/.../008_grokking_module_search_path
- **/home/ubuntu/.../delete_me/**
- /home/ubuntu/.local/share/uv/python/cpython-3.14.1-linux-x86_64-gnu/lib/python314.zip
- /home/ubuntu/.local/share/uv/python/cpython-3.14.1-linux-x86_64-gnu/lib/python3.14
- /home/ubuntu/.local/share/uv/python/cpython-3.14.1-linux-x86_64-gnu/lib/python3.14/lib-dynload
- /home/ubuntu/.../008_grokking_module_search_path/.venv/lib/python3.14/site-packages

Note the second entry.

This will allow you to create a bare file `mymath.py` within the `delete_me/` directory, import it into your program, and consume it.

```bash
PYTHONPATH="/home/ubuntu/Development/git-repos/side-projects/delete_me/" uv run main.py
The area of a circle with radius 5 is 78.53975
```

However, this approach is quite hacky and while the module would be potentially reusable, it wouldn't follow the expected standard to being able to eventually publish it in a repository.

A more manageable approach would be to rely on `uv` and list `mymath` as a dependency.

The first naive approach would be to create a Python project such as the following:

```
./00_my_math_prj
├── __init__.py
├── my_math_thingies.py
├── pyproject.toml
└── uv.lock
```

With `__init__.py` being:

```python
"""mymath package initialization file."""

from my_math_thingies import area

__all__ = ["area"]
```

You could potentially think that then you would be able to do:

```bash
uv add --editable <path-to-my-math>
```

However, your program would fail when doing:

```bash
from mymath import area
```

And it would work when doing:

```bash
from my_math_thingies import area
```

This is because when creating reusable modules, you should follow certain conventions with the folders of your packages.

Instead, you can do:

```
mymath/
├── main.py
├── mymath/
│   ├── __init__.py
│   └── my_math_thingies.py
├── pyproject.toml
└── uv.lock
```

Then, you would be able to use the regular imports.



## Running the program

See [README.md](../README.md#008-grokking-the-module-search-path) for full details.

To run the application with the module dependency, you need to extract `mymath.tgz` and possibly update the path to it in your `pyproject.toml`

```bash
$ cd delete_me
$ tar xvf mymath.tgz
```

```toml
[tool.uv.sources]
mymath = { path = "../../../../../../mymath", editable = true }
```

```bash
uv run main.py
```

