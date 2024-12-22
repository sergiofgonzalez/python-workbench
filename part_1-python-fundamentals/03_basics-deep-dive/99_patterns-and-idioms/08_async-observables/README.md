# Async observables
> illustrating how to extend `EventEmitter` to create observable objects

## Program description

Create a class `RegexFinder` that inherits from `EventEmitter` so that you can invoke it as:

```python
    str_finder = FindRegex(r"(h|H)ello")
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