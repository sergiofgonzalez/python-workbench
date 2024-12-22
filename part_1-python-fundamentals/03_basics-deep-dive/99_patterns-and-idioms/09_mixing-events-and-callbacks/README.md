# Mixing events and callbacks


In this program we create a version of the `find_regex()` function that apart from returning an `EventEmitter` allows the consumer to pass a callback to get the whole list of results.

```python
    str_finder = FindRegex(r"aiofiles", lambda results: print(results))
    str_finder.add_file("pyproject.toml")
    str_finder.add_file("uv.lock")
    str_finder.add_file("README.md")
    str_finder.add_file("non-existent-file.txt")
    str_finder.on("fileread", lambda file: print(f"About to scan {file}"))
    str_finder.on(
        "found",
        lambda file, line, match: print(f"HIT: {file}: {match!r} found in {line!r}"),
    )
    str_finder.on(
        "error",
        lambda err_message: print(
            f"ERROR: error found while scanning for matches: {err_message}",
        ),
    )
    await str_finder.find()
```