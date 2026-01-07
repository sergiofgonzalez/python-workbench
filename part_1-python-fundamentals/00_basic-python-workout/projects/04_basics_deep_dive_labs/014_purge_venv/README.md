# 014: purge_venv
> Purging virtual env directories to reclaim disk space

## Solution

The first interesting part about the project is that in order to make the UX more professional, we included a SIGINT handler in `main.py`. This will let you capture the user pressing CTRL+C to abort, so that no Python code from the program is displayed on the CLI:

```python
def handle_sigint(signum: int, frame: object) -> None:  # noqa: ARG001
    """Handle SIGINT (Ctrl+C) gracefully."""
    print("\n\nOperation cancelled by user.")
    sys.exit(0)


signal.signal(signal.SIGINT, handle_sigint)
```

You can use `signal` module to delegate the handling of the SIGINT signal to the `handle_sigint()` function. Within the function, you simply can print a message, supressing any ugly messages in the terminal.


Another interesting part of the program is the addition of a confirmation from the user. It's a good practice for a script that carries out non-recoverable actions to allow the user to review what's about to be done, so that they can cancelled the operation.

```python
print("This action would delete the above virtual environment directories.")
confirmation = input("Are you sure you want to proceed? (y/N): ").strip().lower()
if confirmation == "y":
    if not args.dry_run:
        err_messages = delete_dirs(venv_dirs_found)
        report_purge_completion(err_messages)
        report_dir_size_before_after_purge(root_dir, before=False)
    else:
        print("Dry run complete. No directories were deleted.")
else:
    print("Purge cancelled by user.")
    return
```

Note that this is intertwined with the `--dry-run` argument that follows through the process without actually deleting anything.

Another argument the program defines is `--venv-names` which allows the user to pass one or more environment variable names (such as `.venv`, `venv`, etc.).

When processing the search for virtual environments, those values are considered, as can be seen on [`dirutils.py`](src/purge_venv/utils/dirutils.py):

```python
def find_venv_dirs(root_dir: Path, venv_names: list[str]) -> list[Path]:
    found_dirs = []
    root_path = Path(root_dir)

    for venv_name in venv_names:
        for venv_path in root_path.rglob(venv_name):
            if venv_path.is_dir():
                found_dirs.append(venv_path)  # noqa: PERF401

    return sorted(found_dirs)
```

As you need to find the virtual environments recursively, from the given root directory, you need to rely on `rglob()`. For the implementation, you can either, run `rglob()` for each of the environment variable names passed, or run `rglob("*")` and then filter out the ones that do not match the given env names. In this case, the first approach is cleaner.

In the same file, the way to cleanly remove the directories and corresponding files is with `shutil.rmtree()`:

```python
def delete_dirs(directories: list[Path]) -> list[str]:
    err_messages = []
    for venv_dir in directories:
        try:
            shutil.rmtree(venv_dir)
        except Exception as e:  # noqa: BLE001
            err_messages.append(f"Error deleting {venv_dir}: {e}")
            print(f"Error deleting {venv_dir}: {e}")
    return err_messages
```

### tests

In the tests, you can create a file to test the [`utils.py`](src/purge_venv/utils/) public interface, and another file to test the end-to-end logic included in [`main.py`](src/purge_venv/main.py) (such as the confirmation logic, arguments, etc.).

There's nothing new on [`test_utils.py`](tests/unit/test_utils.py). The usual pytest provided fixtures such as `tmp_path` and `capsys` are being used to generate ephemeral virtual environments so that you can test your logic, and `capsys` to ensure that whatever is printed onto the terminal makes sense. For example:

```python
def test_report_dir_size_before_after_purge(
    capsys: pytest.CaptureFixture,
    tmp_path: Path,
) -> None:
    """Test reporting directory size before and after purge."""
    venv_dir = tmp_path / "venv"
    venv_dir.mkdir()
    (venv_dir / "file1.txt").write_text("a" * 100)  # 100 bytes
    (venv_dir / "file2.txt").write_text("b" * 200)  # 200 bytes

    report_dir_size_before_after_purge(venv_dir, before=True)
    captured = capsys.readouterr()
    assert "before purge: 300.00 B" in captured.out
    report_dir_size_before_after_purge(venv_dir, before=False)
    captured = capsys.readouterr()
    assert "after purge: 300.00 B" in captured.out
```

The pytest features used in [`test_main.py`](tests/unit/test_main.py) are far more interesting.

In the first block, we confirm that the CLI tool accepts the expected arguments. These set of tests can be used to confirm the stability of the CLI arguments after improvements and refactoring.

The way to test them is to rely on `pytest.MonkeyPatch` to inject to the tool a tailored set of `sys.argv` arguments. For example, for the `--dry-run` argument:

```python
def test_accepts_dry_run_flag(
    tmp_path: str,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture,
) -> None:
    """Test that the CLI accepts --dry-run flag."""
    monkeypatch.setattr(sys, "argv", ["purge-venv", "--dry-run", str(tmp_path)])
    main()
    captured = capsys.readouterr()
    assert "Dry run mode enabled" in captured.out
```

Similarly for `--venv-names`. Note that because you can pass a variable number of venv names, you must pass the directory as the first argument:

```python
def test_accepts_venv_names_option(
    tmp_path: str,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test that the CLI accepts --venv-names option."""
    monkeypatch.setattr(
        sys,
        "argv",
        ["purge-venv", str(tmp_path), "--venv-names", ".venv", "venv"],
    )
    main()  # Should not raise
```

In the second set of tests, we validate the expected behavior when the user is asked for confirmation. The first thing we do is set up a custom fixture using `@pytest.fixture` decorator to set up a sample venv. Thus, we will be able to set up a temporary directory on any of the subsequent test functions by simply using the function name as a parameter.

```python
@pytest.fixture
def dir_with_venv(tmp_path: Path) -> Path:
    """Create a temporary directory with a .venv subdirectory."""
    venv_dir = tmp_path / ".venv"
    venv_dir.mkdir()
    # Add a file inside to make it non-empty
    (venv_dir / "pyvenv.cfg").write_text("home = /usr/bin/python3")
    return tmp_path
```

For example, this function will check that the purge is completed successfully when the user types "y":

```python
def test_deletes_venv_when_user_confirms_with_lowercase_y(
    dir_with_venv: Path,  # custom fixture
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture,
) -> None:
    """Test that venv is deleted when user types 'y'."""
    monkeypatch.setattr(sys, "argv", ["purge-venv", str(dir_with_venv)])
    monkeypatch.setattr("builtins.input", lambda _: "y")
    main()
    captured = capsys.readouterr()
    assert "Purge complete" in captured.out
    assert not (dir_with_venv / ".venv").exists()
```

You start by declaring the `dir_with_venv` fixture. That will make the function `dir_with_venv()` execute before the test, effectively creating a sample `.venv` in a temporary path.

You also declare the `monkeypatch` and `capsys` fixtures to be able to tailor `sys.argv` and the `input()` function.

In particular, as we need to emulate the user typing "y", we use:

```python
monkeypatch.setattr("builtins.input", lambda _: "y")
```

Then, we invoke `main()` and confirm the purging is carried out successfully.


## Running the program

See [README.md](../README.md#014-purge_venvsh-in-python) for full details.

Examples about how to run it.

You can run the application with:

```bash
# run without params
uv run purge-venv

# run to get some help
uv run purge-venv --help

# run on data/ directory with default params
uv run purge-venv data/

# run on data/ directory with non-default venv names
uv run purge-venv data/ --venv-names .venv venv

# dry-run mode (does not delete anything)
vuv run purge-venv data/ --venv-names .venv venv --dry-run
```
