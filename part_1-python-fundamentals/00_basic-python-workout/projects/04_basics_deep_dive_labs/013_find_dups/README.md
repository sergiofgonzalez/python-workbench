# 013: find duplicate files in a directory tree
> scans a directory tree identifying duplicate files

## Solution

As with most of the simple CLI tools, you start by importing `argparse` and declaring your arguments.

In this case, you need to support:
+ the directory which will be taken as the root for finding duplicate files.
+ an optional + `-e/--extensions` that must accepts one or more extensions as in:

    ```
    -e .txt,.out,.log
    ```

    To support that, you need to use:

    ```python
    parser.add_argument(
        "-e",
        "--extensions",
        type=str,
        nargs="+",
        help="List of file extensions to include in the search.",
    )
    ```

Then, you parse the arguments receive, normalize the extensions to simplify the logic, and validate that the received first argument is viable directory (it must be a directory and it must exist).

From there, you just find the duplicates and print them:

```python
args = parser.parse_args()
directory = Path(args.directory)
extensions = normalize_extensions(args.extensions) if args.extensions else None
fail_if_invalid(directory)

duplicates = find_potential_duplicates(directory, extensions)
print(format_duplicate_report(duplicates))
```

Then, the important logic of the program is performed within the `utils/` directory.

The first thing you must notice is that you must include a `__init__.py`. This time, you use `__all__` to identify the *exposed functions*: a sort of public interface of all the stuff you have in `utils/`.

```python
"""__init__.py file for the utils package."""

from utils.fileutils import DupFileReasonEnum, find_potential_duplicates
from utils.report import format_duplicate_report
from utils.validation import fail_if_invalid, normalize_extensions

__all__ = [
    "DupFileReasonEnum",
    "fail_if_invalid",
    "find_potential_duplicates",
    "format_duplicate_report",
    "normalize_extensions",
]
```

That will allow `main.py` to use simpler imports:

```python
from utils import (
    fail_if_invalid,
    find_potential_duplicates,
    format_duplicate_report,
    normalize_extensions,
)
```

And will give you much more freedom to distribute your logic in different files.

`validation.py` includes the logic to normalize the extensions received in the `-e/--extensions` parameter and the function to fail if the argument received for the directory is not viable.

`fileutils.py` is the module in charge of coordinating the files and returning a structure to `main()`.

The file starts with the definition on the different tyes of potential duplicates the script will identify:

```python
class DupFileReasonEnum(Enum):
    """Enum for potential duplicate file reasons."""

    SAME_SIZE_AND_HASH = "same size and hash"
    SAME_NAME = "same name"
    SAME_STEM_DIFF_SUFFIX = "same stem different suffix"
```

Using an enum will simplify the operations and prevent having a mutual understanding based on strings in different parts of the program.

Then, you find the `get_files()` function, which retrieves the files from the directory, optionally filtered by the extensions given as a parameter:

```python
def get_files(directory: Path, extensions: list[str] | None = None) -> list[Path]:
    return [
        f
        for f in directory.rglob("*")
        if f.is_file() and (extensions is None or f.suffix in extensions)
    ]
```

The function is practically a one-liner, but it makes sense to give it a name, so that it's easier to understand. It is using `directory.rglob()` because it has to traverse the directories recursively.

Unfortunately, `rglob()` doesn't support file patterns such as `*[.txt,.log,.out]` so the filtering has to be performed manually.

The next function is `find_potential_duplicates()`. This function orchestrates all the different strategies that will be used to identify potential duplicates:

```python
def find_potential_duplicates(
    directory: Path,
    extensions: list[str] | None = None,
) -> dict[DupFileReasonEnum, dict[str, list[Path]]]:
    files = get_files(directory, extensions)
    by_size_dups_dict = prune_non_duplicates(get_files_by_size(files))
    by_md5_dups_dict = prune_non_duplicates(get_files_by_hash(by_size_dups_dict))
    by_name_dups_dict = prune_non_duplicates(get_files_by_name(files))
    by_stem_dups_dict = prune_non_duplicates(get_files_by_stem_diff_suffix(files))

    return {
        DupFileReasonEnum.SAME_SIZE_AND_HASH: by_md5_dups_dict,
        DupFileReasonEnum.SAME_NAME: by_name_dups_dict,
        DupFileReasonEnum.SAME_STEM_DIFF_SUFFIX: by_stem_dups_dict,
    }
```

The approach is:
1. Get the list of all the files.
1. Find the potential duplicates by identifying the files having the same size. This requires building a dictionary whose string is the file size, and as value, the list of files having that size. Obviously, the keys having a single file in that list can be pruned, as they are unique.
1. Find the potential duplicates by identifying the files having the same hash. Because two files will have the same hash only if they have the same size, you can optimize the processing by having at look only the files having the same size. Also, you can prune the keys having a single file in the list, as they are unique.
1. Find the potential duplicates by looking at the file names. The idea is that you might have the same file name with different hash (e.g., picture/video file with different quality), but it's useful to know you have two files with the same name.
1. Find the potential duplicates by looking at the file stems (file name without extension). Similarly, the idea is you might have the same file with different format (e.g., jpeg and png).

With all the dictionaries of type `dict[str | int, list[Path]]` ready, you can return the result to the caller, with each type of duplicate identified by an enaum value.

The file `file_dict_utils.py` is the one featuring all the functions `find_potential_duplicates()` rely on.

The first one you find is `get_files_by_size()`:

```python
def get_files_by_size(files: list[Path]) -> dict[int, list[Path]]:
    size_dict: dict[int, list[Path]] = {}
    for file in files:
        size = file.stat().st_size
        if size not in size_dict:
            size_dict[size] = []
        size_dict[size].append(file)
    return size_dict
```

You define an empty dictionary and simply create a new key (if it's the first time you see that key) or append the found file to the corresponding key.

The function `prune_non_duplicates()` is the function that is used to remove the dictionary entries with a single key (no matter if the key is name, stem, hash, or size):

```python
def prune_non_duplicates(
    files_dict: dict[Any, list[Path]],
) -> dict[Any, list[Path]]:
    return {metric: files for metric, files in files_dict.items() if len(files) > 1}
```

You use a one-liner, dict comprehension, but as before, it's useful to give it a proper name.

Then, you have `get_files_by_hash()`:

```python
def get_files_by_hash(
    files_by_size_dict: dict[int | str, list[Path]],
) -> dict[str, list[Path]]:
    hash_dict: dict[str, list[Path]] = {}

    for files in files_by_size_dict.values():
        for file in files:
            hasher = hashlib.md5()  # noqa: S324
            with file.open("rb") as f:
                # Read the file in chunks to avoid memory issues with large files
                for chunk in iter(lambda: f.read(4096), b""):
                    hasher.update(chunk)
            file_hash = hasher.hexdigest()
            if file_hash not in hash_dict:
                hash_dict[file_hash] = []
            hash_dict[file_hash].append(file)

    return hash_dict
```

This one is a bit more contrived, as the hashing the file contents requires more care.

You first need to declare the empty dictionary you'll use to group the files by hash.
Then, you start iterating over the list of files. Because the list of files has been pruned, you can blindly go over each of the lists received.

For each of the files, you need to:
1. Get an MD5 hasher by calling `hashlib.md5()`.
1. Open the file in `"rb"` mode with a context manager
1. Read the file in chunks of 4K bytes, and for each chunk update the hash.
1. Once you're done reading the file, you can get the string representation using `hasher.hexdigest()`.
1. Then, you either create a new entry in the resulting dict if it's the first time you see it, or append the file to the existing list for the hash.


Then you have the `get_files_by_name()` function. This one is in charge of returning a dictionary where the files are grouped by their name, without minding the path to the file:

```python
def get_files_by_name(files: list[Path]) -> dict[str, list[Path]]:
    name_dict: dict[str, list[Path]] = {}
    for file in files:
        name = file.name
        if name not in name_dict:
            name_dict[name] = []
        name_dict[name].append(file)
    return name_dict
```

The `file.name` is the way to get the name and extension of the file.

Finally, you have the `get_files_by_stem_diff_suffix()`. The interesting part about this one is that because the files with the same stem will already be collected by `get_files_by_name()`, you need to make sure that you only include the files having the same stem (name without extension) and having different extension.

```python
def get_files_by_stem_diff_suffix(files: list[Path]) -> dict[str, list[Path]]:
    stem_dict: dict[str, list[Path]] = {}
    for file in files:
        stem = file.stem
        if stem not in stem_dict:
            stem_dict[stem] = []
        suffixes = {f.suffix for f in stem_dict[stem]}
        if file.suffix not in suffixes:
            stem_dict[stem].append(file)
    return stem_dict
```

The easier way to do that is to make sure that you add to the dictionary the entries that have a different extension. For that, before adding the file to the list of paths associated to a key, you create a set with their suffixes and make sure that you only add the file if the suffix is not there. This might not be the most optimized way to do so, but it's easy to understand and program.

Finally, the `report.py` includes the logic to create the report, which is implemented by the `format_duplicate_report()` function:

```python
def format_duplicate_report(
    duplicates: dict[DupFileReasonEnum, dict[str, list[Path]]],
) -> str:
    report_lines = []
    for reason, files_dict in duplicates.items():
        report_lines.append(f"Reason: {reason.value}")
        if not files_dict:
            report_lines.append("    No potential duplicates found.\n")
            continue
        for _, files in files_dict.items():  # noqa: PERF102
            report_lines.extend([f"    - {file}" for file in files])
            report_lines.append("")  # Add an empty line between groups of duplicates
        report_lines.append("")  # Add an empty line between reasons
    return "\n".join(report_lines)
```

The report structure is very simple:

```
Reason: same size and hash
    - data/some_other_file.txt
    - data/some_file.txt
    - data/yet_another_file.txt
    - data/subdir_1/yet_another_file.out
    - data/subdir_2/some_other_file.txt

    - data/file_3.out
    - data/subdir_2/file_21.out

    - data/subdir_1/file_11.txt
    - data/subdir_1/subdir_11/file_112.txt


Reason: same name
    - data/some_other_file.txt
    - data/subdir_2/some_other_file.txt

    - data/some_file.txt
    - data/subdir_1/subdir_11/some_file.txt


Reason: same stem different suffix
    - data/some_file.txt
    - data/subdir_1/some_file.out

    - data/yet_another_file.txt
    - data/subdir_1/yet_another_file.out
```

You get, a heading with all the different groupings (same hash, same name, same stem), and then a list of newline separated list of paths.

Note that hashes, sizes, and even names are not printed.

### tests

For the tests, you can focus on testing the *public interface* of the `utils` module.

No major new tricks used in these tests: `tmp_path` pytest fixture is used to set up different file structures to validate the results.

Also, during the assertions for some of the cases, the dictionary `popitem()` method is used, which returns the last key-value pair added to the dictionary.

Because the files are created by way of pytest fixture, it's more than possible that tests become flaky. To make them more stable, you'd just need to precalculate the hashes, sizes, etc. to make them more predictable.

### publising as a tool

To publish find_dups in the package repository (PyPI) it's recommended to start with a brand new directory for the project.

That way, you will be able to evolve and adjust details separately from the rest of the lab examples, and it won't take that much time.

Therefore, you should start by creating a directory for find_dups.

```bash
mkdir find-dups
```

It's quite common to name the package with regular dashes instead of underscore.

Then, you can use `uv` to create the structure that will allow you to publish the package easily:

```bash
uv init --package find-dups
```

The command will create a slightly different structure than the one used in the labs, but it's very recognizable. The difference is that you have a `src/find_dups` directory in which you should place all the lab's files.

Because of the different structure, you will also need to adjust the imports, starting with the module that contained all the utilities:

```python
from find_dups.utils.fileutils import DupFileReasonEnum, find_potential_duplicates
from find_dups.utils.report import format_duplicate_report
from find_dups.utils.validation import fail_if_invalid, normalize_extensions

__all__ = [
    "DupFileReasonEnum",
    "fail_if_invalid",
    "find_potential_duplicates",
    "format_duplicate_report",
    "normalize_extensions",
]
```

Same will apply to the rest of the files, all the previous `from utils.*` will have to be updated to `from find_dups.utils.*`.


As the next step, you shoul also transfer the tests. You can copy the `tests/` directories to a new `tst/` (as the source is `src/`). You must also update the imports as you did in the previous step.

Then, you will have to update `pyproject.toml`. `uv init` will already have created a file for you, but you will have to transfer all the settings from the lab, and also adjust the pytest related tests as they're now placed in a `tst/` directory:

```toml
[project]
name = "find-dups"
version = "0.1.0"
description = "Simple tool to find duplicate files in a directory tree."
readme = "README.md"
authors = [
    { name = "Sergio F. Gonzalez", email = "sergio.f.gonzalez@gmail.com" },
]
requires-python = ">=3.12"
dependencies = []

[dependency-groups]
dev = [
    "pytest>=9.0.2",
    "ruff>=0.14.8",
    "pytest-cov>=7.0.0",
    "pytest-sugar>=1.1.1",
]

[project.scripts]
find-dups = "find_dups.main:main"

[build-system]
requires = ["uv_build>=0.9.15,<0.10.0"]
build-backend = "uv_build"

[tool.ruff]
ignore = [
    "T201", # Allow print statements
]

# Enable all rules
select = ["ALL"]

# Specific per-file-ignores for the tests directory
per-file-ignores = { "tst/**/*.py" = ["S101"] } # Allow assert in tests

[tool.ruff.lint.pydocstyle]
convention = "google"

[tool.pytest.ini_options]
addopts = "--verbosity=3 --cov --cov-report=html"
pythonpath = ["."]

[tool.coverage.run]
omit = ["tst/*"]
```

The other interesting part is the scripts section:

```bash
[project.scripts]
find-dups = "find_dups.main:main"
```

That part will enable your users to invoke the script as:

```bash
$ find-dups
```

instead of

```bash
$ uv run src/find_dups/main.py
```

which will also work.


At this point, you will be able to test whether the package can be built successfully by running `uv build`:

```bash
$ uv build
Building source distribution (uv build backend)...
Building wheel from source distribution (uv build backend)...
Successfully built dist/find_dups-0.1.0.tar.gz
Successfully built dist/find_dups-0.1.0-py3-none-any.whl
```

Sooo simple! Kudos to the `uv` team for making the package creation such a simple activity.

Then, you will need to add the bells and whistles such as adding a changelog file, and a license file.

At this point, you'll be ready to create a GitHub repo and push your initial version.

It's a good practice to publish first on https://test.pypi.org to confirm that your package works as expected.

In order to do so, it's a good option to update the package version to something like `0.1.0-rc1` in `pyproject.toml`. This will ensure that you can fix things on 0.1.0 without bumping the version.

Publishing in test.pypi will require you to login, and possible generate a new token with sufficient permissions to publish a new package (there are other tokens that can be created with per-project scope).

With a token at hand, you will be able to publish by doing:

```bash
# Clean the dist directory
$ rm -rf dist/

# Rebuild the package
$ uv build

# Publish to test.pypi.org
$ uv publish \
  --publish-url https://test.pypi.org/legacy/ \
  --token <token>
Publishing 2 files to https://test.pypi.org/legacy/
Uploading find_dups-0.1.0rc1.tar.gz (3.4KiB)
Uploading find_dups-0.1.0rc1-py3-none-any.whl (5.8KiB)
```

Once published you can go to https://test.pypi.org/project/find-dups/ and your recently published package will be there.

Then, it's necessary to test it works. Because it's published on test.pypi, you will need to use an extra argument. It's a good idea to test it from a new directory (not in your labs). You can copy the `data/` directory there:

```bash
# cd into a new dir (not the labs one)
$ cd some_random_dir

# copy the data
$ cp -rf path/to/data .

# run with uvx
uvx --index https://test.pypi.org/simple find-dups data
```

That should render the same results as in the lab.


If everything goes well, only the finishing touches will remain.

First, you will need to remove the -rc1 from the version, as you're now ready to publish the 0.1.0 version.

Then, you should commit and push all your changes to GitHub to make sure the published version is in sync with whatever you publish. To inform GitHub of your release, it's a good idea to create a tag and push it:

```bash
# tag the latest commits
$ git tag v0.1.0

# push the tags
$ git push --tags
```

Now, you just need to republish, but this time on the production PyPI. As before, you'll need to get a token first. Once you have it, you just need to do:

```bash
# Clean the dist directory
$ rm -rf dist/

# Rebuild the package
$ uv build

# Publish to test.pypi.org
$ uv publish --token <token>
Publishing 2 files to https://upload.pypi.org/legacy/
Uploading find_dups-0.1.0.tar.gz (3.4KiB)
Uploading find_dups-0.1.0-py3-none-any.whl (5.8KiB)
```

Now you can test it with no extra args:

```bash
# run with uvx
uvx find-dups data
```

And you will be able to find your recently published package in https://pypi.org/project/find-dups/


## Running the program

See [README.md](../README.md#013-find-duplicates-in-a-directory-tree) for full details.

You can run the application with:

```bash
uv run main.py
```

