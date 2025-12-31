# 012: Calculating directory tree size
> calculate the total size of all files that aren't symlinks in a directory tree.

## Solution

The program is a command-line script, written on a single `main.py` file.
The `main()` function orchestrates the whole execution:

```python
def main() -> None:
    """Application entry point."""
    parser = argparse.ArgumentParser(
        description="Calculate the size of a directory tree.",
    )
    parser.add_argument("directory", type=str, help="Path to the directory to analyze.")
    parser.add_argument(
        "-e",
        "--extension",
        type=str,
        help="Filter files by extension.",
        default=None,
    )
    parser.add_argument(
        "--human-readable",
        action="store_true",
        help="Display size in a human-readable format (e.g., KB, MB).",
    )
    args = parser.parse_args()

    dir_tree = Path(args.directory)
    validate(dir_tree)

    total_size = get_directory_size(dir_tree, args.extension)
    print_results(
        total_size=total_size,
        directory=args.directory,
        extension=args.extension,
        human_readable=args.human_readable,
    )
```

First, you need to use `argparse` module to declare the arguments the tool will accept:
+ directory: required positional argument.
+ -e/--extension: an optional named argument to filter by extension (as in `.py`).
+ --human-readable: an optional named argument to report size in KB, MB, etc.

With the arguments in place, you have to:
+ parse arguments
+ validate that the required positional argument is valid (it must be an existing directory).
+ get the directory size, by delegating the calculation to `get_directory_size()`.
+ print the results.

The function `get_directory_size()` is in charge of accumulating the size of all the files in the given directory.

```python
def get_directory_size(directory: Path, extension: str | None = None) -> int:
    total_size = 0
    pattern = f"*{extension}" if extension else "*"
    for fp in directory.rglob(pattern):
        if fp.is_file():
            total_size += fp.stat().st_size
    return total_size
```

Because you might need to filter files by extension, you use `Path.rglob()` to get the directory entries. The pattern is adjusted as follows:
+ if extension is given, the pattern `*{extension}` is used.
+ if no extension is given, `*` is used.

Then, for each directory entry, you need to check if it's a file, and if so, we accumulate on the `total_size`.

The function `get_human_readable_size()` is in charge of getting a given size in bytes and returning a string representing the same size as a size in bytes, kbytes, etc.

```python
def get_human_readable_size(size_in_bytes: int) -> str:
    size = size_in_bytes
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size < 1024:  # noqa: PLR2004
            return f"{size:.2f} {unit}"
        size /= 1024
    return f"{size:.2f} PB"
```

The algorithm is:
1. Loop over the size units you support: B, KB, MB, ...
1. Inspect the size.
  1. If it's smaller than 1024 ($ 2^{10} $), you return the size and the unit.
  1. If it's larger than 1024, you need to divive it by 1024 and iterate again.
1. If you get to the end on the loop, you report the size in PB.


The `print_results()` function is the one in charge of reporting the size based on the arguments received:

```python
def print_results(
    *,
    total_size: int,
    directory: str,
    extension: str | None,
    human_readable: bool,
) -> None:
    report_fixed_part = (
        f"Total size of files in '{directory}'"
        f"{' with extension ' + repr(extension) if extension else ''}: "
    )
    if human_readable:
        human_readable_size = get_human_readable_size(total_size)
        print(f"{report_fixed_part}{human_readable_size}")
    else:
        print(
            f"{report_fixed_part}{total_size} {'byte' if total_size == 1 else 'bytes'}",
        )
```

It's doing some basic string management based on the variations you might receive:
+ Did you receive extension?
+ Did you need to use the bytes or the human-readable output?
+ In the case of bytes reporting: do you need to use the singular (1 byte) or the plural (0 bytes)

Finally, the `validate()` function checks that the received argument is a valid directory.

```python
def validate(directory: Path) -> None:
    if not directory.exists():
        print(f"The directory '{directory}' does not exist.")
        sys.exit(1)
    if not directory.is_dir():
        print(f"The path '{directory}' is not a valid directory.")
        sys.exit(1)
```

Because it is a simple script, you can simply exit when something is not according to your expectations.

### pytest

The whole script is included in `main.py`, therefore, the tests will need to import from `main` as if it were a module:

```python
from main import (
    get_directory_size,
    get_human_readable_size,
    main,
    print_results,
    validate,
)
```

The first thing you can test is the `validate()` function. You have to test both for making sure the program exits when passed a non-existent directory, or a path to something that is not a directory. It's better to separate both on their own test function:

```python
def test_validate_with_nonexistent_directory() -> None:
    """Test validate function with a non-existent directory."""
    with (
        patch("pathlib.Path.exists", return_value=False) as mock_exists,
        patch("sys.exit", side_effect=SystemExit) as mock_exit,
    ):
        with pytest.raises(SystemExit):
            validate(Path("fake/path"))
        mock_exists.assert_called_once()
        mock_exit.assert_called_once_with(1)
```

You can use `patch()` with the context manager to alter the behavior of `Path.exists()` by returning `False`, no matter what it is passed and `sys.exit()` to raise a `SystemExit`.

Then, we confirm that calling validate fails with a `SystemExit()`, and that `sys.exit()` is called once with `1`, and that `exists()` is also being called. The latter to ensure that if `validate()`'s implementation changes, we get a failed test and can update the test too.

Similarly, when testing with a valid path to something that is not a dir:

```python
def test_validate_with_non_directory_path() -> None:
    """Test validate function with a path that is not a directory."""
    with (
        patch("pathlib.Path.exists", return_value=True) as mock_exists,
        patch("pathlib.Path.is_dir", return_value=False) as mock_is_dir,
        patch("sys.exit", side_effect=SystemExit) as mock_exit,
    ):
        with pytest.raises(SystemExit):
            validate(Path("fake/path"))
        mock_exists.assert_called_once()
        mock_is_dir.assert_called_once()
        mock_exit.assert_called_once_with(1)
```

Finally, we test the happy path:

```python
def test_validate_with_valid_directory() -> None:
    """Test validate function with a valid directory."""
    with (
        patch("pathlib.Path.exists", return_value=True) as mock_exists,
        patch("pathlib.Path.is_dir", return_value=True) as mock_is_dir,
        patch("sys.exit") as mock_exit,
    ):
        validate(Path("valid/path"))
        mock_exists.assert_called_once()
        mock_is_dir.assert_called_once()
        mock_exit.assert_not_called()
```

Then you can tackle the `get_directory_size()` function. The possible scenarios are:
+ the function finds an empty directory, and should return 0.
+ the function finds some files and should return the sum of their sizes.
+ the function is given extension, and must return only the sum of the files that match the passed extension (empty, some files, and all files).

The first scenario is the simplest one:

```python
def test_get_directory_size_empty_directory() -> None:
    """Test get_directory_size with an empty directory."""
    with patch("pathlib.Path.rglob", return_value=iter([])) as mock_rglob:
        size = get_directory_size(Path("empty/dir"))
        assert size == 0
    mock_rglob.assert_called_once_with("*")
```

The function `Path.rglob()` returns an iterator of Path objects. As such, it's convenient to use `patch()` with the context manager returning an empty iterator.

Then, you just validate that the function returns 0. Because you're using mocks and have inspected the internals of `get_directory_size()` to understand that `Path.rglob()` is the function to be mocked, we also add an assertion to validate that our `mock_rglob` is called. That way, if the implementation of `Path.rglob()` changes, the test will fail and you could adjust.

For the other scenario the situation is slightly more complex, as you need a supporting test class to make your tests works, the `MockPath` class:

```python
class MockPath:
    """Mock Path object for testing purposes."""

    def __init__(self, size: int, name: str = "file") -> None:
        """Initializes the MockPath with a given size and file name."""
        self._size = size
        self._name = name

    def is_file(self) -> bool:
        """Mock is_file method always returns True."""
        return True

    @property
    def name(self) -> str:
        """Mock name property returns the file name."""
        return self._name

    @property
    def suffix(self) -> str:
        """Mock suffix property returns the file extension."""
        if "." in self._name:
            return "." + self._name.rsplit(".", 1)[-1]
        return ""

    def stat(self) -> object:
        """Mock stat method returns an object with st_size attribute."""

        class StatResult:
            st_size = self._size

        return StatResult()

    def match(self, pattern: str) -> bool:
        """Mock match method to support glob pattern matching."""
        return fnmatch.fnmatch(self._name, pattern)
```

The `MockPath` class is intented to help us tailor the files that `Path.rglob()` will find. As such, `MockPath` is configured with:
+ an initializer method that lets you configure the size and name of the file.
+ an `is_file()` method that will always return `True`.
+ a read-only `name` property that will return the name of the file.
+ a `suffix` property that will return the file's extension if given, or `""` otherwise. The strategy to return the extension is very simple: we split the name by `.` and only once, and return the last component.
+ a `stat()` method that will return a mocked `StatResult` object that will contain only the `st_size` property with the size configured in the initializer.
+ a `match()` method that accepts a `pattern` parameter that will return true if the name of the file matches the given pattern. `Path.rglob()` will call this when we call it with the extension.

With this class in place, you'll have an easier time testing the subsequent scenarios:

```python
def test_get_directory_size_with_files() -> None:
    """Test get_directory_size with files of various sizes."""
    mock_files = [
        MockPath(100, "a.txt"),
        MockPath(200, "b.txt"),
        MockPath(300, "c.txt"),
    ]
    with patch("pathlib.Path.rglob", mock_rglob(mock_files)):
        size = get_directory_size(Path("dir/with/files"))
        assert size == 600  # noqa: PLR2004
```

In the test, you need to arrange the files that should be returned, and configure the `Path.rglob()` mock to return those. Note that you'll need to use a different structure for `patch()`.

This test uses a custom mock factory function `mock_rglob()` instead of the
standard `patch(object, return_value)` approach because:
    1. **Context-aware mocking**: The mock needs to return different results based on the pattern passed to rglob() (e.g., "\*.txt"). A simple return_value cannot handle dynamic behavior based on arguments.

    2. **Stateful iterator behavior**: rglob() returns an iterator/generator that can be consumed. Using mock_rglob() allows creation of a fresh iterator for each call, whereas return_value would return the same exhausted iterator.

    3. **Method chaining**: The mock may need to simulate Path objects with their own methods (like .stat(), .is_file()). A factory function can create properly configured mock objects with the necessary attributes and behaviors.

Similarly for the remaining scenarios:

```python
def test_get_directory_size_with_extension_filter() -> None:
    """Test get_directory_size with an extension filter."""
    mock_files = [
        MockPath(100, "a.txt"),
        MockPath(200, "b.txt"),
        MockPath(300, "c.txt"),
    ]
    with patch("pathlib.Path.rglob", mock_rglob(mock_files)):
        size = get_directory_size(Path("dir/with/files"), extension=".txt")
        assert size == 600  # All files match the extension  # noqa: PLR2004


def test_get_directory_size_with_extension_filter_empty() -> None:
    """Test get_directory_size with an extension filter."""
    mock_files = [
        MockPath(100, "a.txt"),
        MockPath(200, "b.txt"),
        MockPath(300, "c.txt"),
    ]
    with patch("pathlib.Path.rglob", mock_rglob(mock_files)):
        size = get_directory_size(Path("dir/with/files"), extension=".png")
        assert size == 0  # No files match the extension


def test_get_directory_size_with_mixed_files() -> None:
    """Test get_directory_size with mixed files and an extension filter."""
    mock_files = [
        MockPath(100, "a.txt"),
        MockPath(200, "b.png"),
        MockPath(300, "c.txt"),
        MockPath(400, "d.jpg"),
    ]
    with patch("pathlib.Path.rglob", mock_rglob(mock_files)):
        size = get_directory_size(Path("dir/with/files"), extension=".txt")
        assert size == 400  # Only .txt files are counted (100 + 300)  # noqa: PLR2004
```

All the test functions use the same strategy with the `mock_rglob()` factory function.

Then, you can deal with `get_human_readable_size()`. Because the function under test is very simple, you can club all the scenarios in single test function:

```python
def test_get_human_readable_size() -> None:
    """Test get_human_readable_size function."""
    assert get_human_readable_size(0) == "0.00 B"
    assert get_human_readable_size(500) == "500.00 B"
    assert get_human_readable_size(2048) == "2.00 KB"
    assert get_human_readable_size(5 * 1024 * 1024) == "5.00 MB"
    assert get_human_readable_size(3 * 1024 * 1024 * 1024) == "3.00 GB"
    assert get_human_readable_size(7 * 1024 * 1024 * 1024 * 1024) == "7.00 TB"
    assert get_human_readable_size(2 * 1024 * 1024 * 1024 * 1024 * 1024) == "2.00 PB"
```

This is a great test implementation, as it doesn't mock anything.

Then, you can test `print_results()` function. Because this function sends the report to stdout using `print()`, you need to include a `CaptureFixture` so that you can assert what has been sent to the terminal:

```python
def test_print_results(capsys: pytest.CaptureFixture[str]) -> None:
    """Test print_results function."""
    print_results(
        total_size=2048,
        directory="test/dir",
        extension=None,
        human_readable=False,
    )
    captured = capsys.readouterr()
    assert captured.out.strip() == "Total size of files in 'test/dir': 2048 bytes"

    print_results(
        total_size=2048,
        directory="test/dir",
        extension=None,
        human_readable=True,
    )
    captured = capsys.readouterr()
    assert captured.out.strip() == "Total size of files in 'test/dir': 2.00 KB"

    print_results(
        total_size=2048,
        directory="test/dir",
        extension=".txt",
        human_readable=False,
    )
    captured = capsys.readouterr()
    assert (
        captured.out.strip()
        == "Total size of files in 'test/dir' with extension '.txt': 2048 bytes"
    )

    print_results(
        total_size=2048,
        directory="test/dir",
        extension=".txt",
        human_readable=True,
    )
    captured = capsys.readouterr()
    assert (
        captured.out.strip()
        == "Total size of files in 'test/dir' with extension '.txt': 2.00 KB"
    )

    print_results(
        total_size=1,
        directory="test/dir",
        extension=None,
        human_readable=False,
    )
    captured = capsys.readouterr()
    assert captured.out.strip() == "Total size of files in 'test/dir': 1 byte"

    print_results(
        total_size=1,
        directory="test/dir",
        extension=".py",
        human_readable=False,
    )
    captured = capsys.readouterr()
    assert (
        captured.out.strip()
        == "Total size of files in 'test/dir' with extension '.py': 1 byte"
    )
```

The test include multiple scenarios, but all of them follow the same pattern:
1. You call `print_results()` with a different set of arguments.
1. You capture what `print()` has sent to the output using `readouterr()`.
1. You assert the message.

Finally, a few extra tests were included directly on `main()`. This was just some extra effort to increase the overall test coverage metric and requires some new techniques.

Let's start with testing main when sending the `--human-readable` argument:

```python
def test_main_with_human_readable(
    capsys: pytest.CaptureFixture[str],
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test main() with --human-readable flag."""
    test_file = tmp_path / "test.txt"
    test_file.write_text("x" * 1024)  # 1024 bytes

    monkeypatch.setattr("sys.argv", ["main", str(tmp_path), "--human-readable"])
    main()

    captured = capsys.readouterr()
    assert "1.00 KB" in captured.out
```

See that we configure the test function with three fixtures:
+ `capsys`: to capture what `print()` sends to stdout.
+ `tmp_path`: which is configured as a regular path. This will be passed into the function automatically by pytest using a feature called **fixture injection**.

    When pytest sees a test function parameter name that matches a known fixture, it automatically creates and passes the object.

    In this case, this will create a real, temporary directory unique to each test, will pass that directory to the test function and will clean it up after the test finishes.

    These directories will be in temp directories like `/tmp/pytest-of-ubuntu/pytest-123/test_main_with_human_readable0/`.

+ `monkeypatch`: another built-in pytest fixture for temporarily replacing attributes, environment variables, or items during a test.

    `MonkeyPatch` is simpler than `unittest.mock`, but easier to use for simple value replacements.

    Common monkeypatch uses include:
        + `setattr(obj, name, value)`: replace an attribute value like `sys.argv`.
        + `setenv(name, value)`: set an environment variable.
        + `delenv(name)`: deletes an environment variable.
        + `setitem(dict, key, value)`: set a dict key.
        + `chdir(path)` change current working dir.

In the test function implementation, we use the convenient `tmp_path` fixture to write a `test.txt` file with 1024 "x" to have a 1KB file written.

Then, we use the `monkeypatch` fixture to temporarily replace `sys.argv` so that when `main()` runs it receives the arguments:
+ 0: `main`
+ 1: the path to the directory (`tmp_path`)
+ 2: the `--human-readable` option

Then you invoke `main()` and validate that we get 1.00 KB in the output.

Similarly, when using the extension argument:

```python
def test_main_with_extension_filter(
    capsys: pytest.CaptureFixture[str],
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test main() with --extension flag."""
    (tmp_path / "file.txt").write_text("hello")  # 5 bytes
    (tmp_path / "file.py").write_text("print('hi')")  # 11 bytes

    monkeypatch.setattr("sys.argv", ["main", str(tmp_path), "-e", ".txt"])
    main()

    captured = capsys.readouterr()
    assert "5 bytes" in captured.out
```

Note that in this case, we're writing two files, and using `monkeypatch` to pass the `-e` argument with `.txt` extension. This is a sort of robust end-to-end test as doesn't assume any knowledge of how the different functions invoked from `main()` are implemented.

Exactly the same when using both flags:

```python
def test_main_with_both_flags(
    capsys: pytest.CaptureFixture[str],
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test main() with both --human-readable and --extension flags."""
    (tmp_path / "data.txt").write_text("x" * 2048)  # 2048 bytes
    (tmp_path / "script.py").write_text("x" * 1024)  # 1024 bytes

    monkeypatch.setattr(
        "sys.argv",
        ["main", str(tmp_path), "-e", ".txt", "--human-readable"],
    )
    main()

    captured = capsys.readouterr()
    assert "2.00 KB" in captured.out
    assert "'.txt'" in captured.out
```

Finally, we test `main()` with an invalid directory:

```python
def test_main_with_invalid_directory(
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test main() with non-existent directory."""
    monkeypatch.setattr("sys.argv", ["main", "/nonexistent/path"])

    with pytest.raises(SystemExit) as exc_info:
        main()

    assert exc_info.value.code == 1
    captured = capsys.readouterr()
    assert "does not exist" in captured.out
```

And with an existing path that is not a directory, but rather a path to a file:

```python
def test_main_with_path_to_a_file(
    capsys: pytest.CaptureFixture[str],
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test main() with non-existent directory."""
    test_file = tmp_path / "test.txt"
    test_file.write_text("Sample content")
    monkeypatch.setattr("sys.argv", ["main", str(test_file)])

    with pytest.raises(SystemExit) as exc_info:
        main()

    assert exc_info.value.code == 1
    captured = capsys.readouterr()
    assert "is not a valid directory" in captured.out
```



## Running the program

See [README.md](../README.md#012-calculating-directory-tree-size) for full details.

You can run the application with:

```bash
# basic invocation
$uv run main.py data/
Total size of files in 'data/': 1 byte

# requesting human-readable output
$ uv run main.py . --human-readable
Total size of files in '.': 130.30 MB

# filtering files with human-readable output
$ uv run main.py . --human-readable --ext .py
Total size of files in '.' with extension '.py': 6.42 MB

# filtering files
$ uv run main.py . --ext .py
Total size of files in '.' with extension '.py': 6737019 bytes
```

