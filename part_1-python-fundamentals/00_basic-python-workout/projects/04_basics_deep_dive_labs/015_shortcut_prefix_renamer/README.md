# Shortcut Prefix Renamer
> script that renames files that start with a shortcut prefix such as "Link to" or "Shortcut to".

## Solution

Most of the techniques used in this program have already been used in the previous example. The only interesting new thing in this script is the way in which the renaming is being done avoiding file collisions.

That logic is implemented in three functions: `rename_files()`, `rename_file()`, and `generate_candidate_paths()` in [`fileutils.py`](src/shortcut_prefix_renamer/utils/fileutils.py).

The function `rename_files()` is the high-lever orchestrator for the renaming process:

```python
def rename_files(files: list[Path], prefix: str, *, dry_run: bool = False) -> list[str]:
    status_messages = []
    for file_path in files:
        try:
            # Remove the prefix from the filename
            status_message = rename_file(file_path, prefix, dry_run=dry_run)
            status_messages.append(status_message)
        except Exception as e:  # noqa: BLE001
            status_messages.append(f"Error renaming {file_path}: {e}")
            print(f"Error renaming {file_path}: {e}")
    return status_messages
```

It gets the list of files to rename, the prefix, and whether the user opted for the dry run mode. Then, the renaming for each of the files is delegated to `rename_file()` and the status message returned by each individual operation is appended to a list of status messages for reporting.

`rename_file()` is the function doing the actual renaming and controlling there won't be a name collision while renaming.

```python
def rename_file(file_path: Path, prefix: str, *, dry_run: bool = False) -> str:
    new_name = file_path.name[len(prefix) :]
    new_path = file_path.with_name(new_name)

    for candidate_path in generate_candidate_paths(new_path):
        if candidate_path.exists():
            continue
        if not dry_run:
            file_path.rename(candidate_path)
        return f"Renamed: {file_path} -> {candidate_path}"

    return (
        f"Failed to rename {file_path}: could not find a unique name after "
        f"999 attempts."
    )
```

The function begins by identifying what the name should be by trimming the prefix from the name. Then, a for loop is used to attempt names that could be used in the renaming process. The strategy for generating the new name is delegated to `generate_candidate_paths()`, a generator function that will try "Document.txt" for a file named "Link to Document.txt" first, and if a collision is found, will start trying "Document_001.txt", "Document_002.txt", etc.

Note that to identify the name collision `candidate_path.exists()` is used because `file_path.rename(candidate_path)` don't raise a `FileAlreadyExists` exception when a symlink named "Link to Document.txt" and pointing to an existing "Document.txt" is found, which effectively causes the original "Document.txt" file to be deleted!

So, in this particular case, the LBYL (Look Before You Leap) works better than EAFP (Easier to Ask for Forgiveness than Permission).

Thus, `candidate_path.exists()` checks if the candidate name is already present in the directory, and if so, a new name is generated and attempted. If you run out of indices without finding any viable option, the renaming operation won't happen and a status messages explaining the situation will be returned.

The `generate_candidate_paths()` generator is a very convenient construct to return the candidate names.

```python
def generate_candidate_paths(base_path: Path) -> Generator[Path, None, None]:
    """Generate candidate paths: original name, then with _001, _002, etc."""
    yield base_path
    for i in range(1, 1000):
        suffixed_name = f"{base_path.stem}_{i:03d}{base_path.suffix}"
        yield base_path.with_name(suffixed_name)
```

It starts yielding "Document.txt" for a file named "Link to Document.txt". Subsequently, it returns "Document_001.txt", "Document_002.txt", etc.


## Running the program

See [README.md](../README.md#999-TBD) for full details.

Examples about how to run it.

You can run the application with:

```bash
# run the tool without arguments
uv run shortcut-prefix-renamer

# run the tool getting help
uv run shortcut-prefix-renamer --help

# run the tool with default options on data/ directory
uv run shortcut-prefix-renamer data/

# run the tool with a custom prefix on data/ directory
uv run shortcut-prefix-renamer data/ --shortcut-prefix "Shortcut to"

# run the tool on dry-run mode (won't rename anything)
uv run shortcut-prefix-renamer data/ --dry-run
```
