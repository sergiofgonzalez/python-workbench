"""pytest unit tests for creature.py."""

import contextlib
import fnmatch
from collections.abc import Callable, Generator
from pathlib import Path
from unittest.mock import patch

import pytest

from main import (
    get_directory_size,
    get_human_readable_size,
    main,
    print_results,
    validate,
)


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


def mock_rglob(
    mock_files: list[MockPath],
) -> Callable[[object, str], Generator[MockPath, None, None]]:
    """Create a mock rglob function that filters files based on glob pattern."""

    def rglob_func(self: object, pattern: str) -> Generator[MockPath, None, None]:  # noqa: ARG001
        return (f for f in mock_files if f.match(pattern))

    return rglob_func


def test_validate_with_nonexistent_directory() -> None:
    """Test validate function with a non-existent directory."""
    with (
        patch("pathlib.Path.exists", return_value=False),
        patch("sys.exit", side_effect=SystemExit) as mock_exit,
    ):
        with contextlib.suppress(SystemExit):
            validate(Path("fake/path"))
        mock_exit.assert_called_once_with(1)


def test_validate_with_non_directory_path() -> None:
    """Test validate function with a path that is not a directory."""
    with (
        patch("pathlib.Path.exists", return_value=True),
        patch("pathlib.Path.is_dir", return_value=False),
        patch("sys.exit", side_effect=SystemExit) as mock_exit,
    ):
        with contextlib.suppress(SystemExit):
            validate(Path("fake/path"))
        mock_exit.assert_called_once_with(1)


def test_validate_with_valid_directory() -> None:
    """Test validate function with a valid directory."""
    with (
        patch("pathlib.Path.exists", return_value=True),
        patch("pathlib.Path.is_dir", return_value=True),
        patch("sys.exit") as mock_exit,
    ):
        validate(Path("valid/path"))
        mock_exit.assert_not_called()


def test_get_directory_size_empty_directory() -> None:
    """Test get_directory_size with an empty directory."""
    with patch("pathlib.Path.rglob", return_value=iter([])):
        size = get_directory_size(Path("empty/dir"))
        assert size == 0


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


def test_get_human_readable_size() -> None:
    """Test get_human_readable_size function."""
    assert get_human_readable_size(0) == "0.00 B"
    assert get_human_readable_size(500) == "500.00 B"
    assert get_human_readable_size(2048) == "2.00 KB"
    assert get_human_readable_size(5 * 1024 * 1024) == "5.00 MB"
    assert get_human_readable_size(3 * 1024 * 1024 * 1024) == "3.00 GB"
    assert get_human_readable_size(7 * 1024 * 1024 * 1024 * 1024) == "7.00 TB"
    assert get_human_readable_size(2 * 1024 * 1024 * 1024 * 1024 * 1024) == "2.00 PB"


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
