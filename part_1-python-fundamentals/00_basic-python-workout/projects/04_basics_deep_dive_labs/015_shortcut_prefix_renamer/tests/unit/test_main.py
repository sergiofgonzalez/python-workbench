"""Unit tests for main (end-to-end testing)."""

import os
import signal
import sys
from pathlib import Path

import pytest

from shortcut_prefix_renamer.main import main


def test_accepts_directory_argument(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture,
) -> None:
    """Test that the CLI accepts a directory argument."""
    monkeypatch.setattr(sys, "argv", ["shortcut-prefix-renamer", str(tmp_path)])
    main()
    captured = capsys.readouterr()
    assert "No files to rename" in captured.out


def test_accepts_dry_run_flag(
    tmp_path: str,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture,
) -> None:
    """Test that the CLI accepts --dry-run flag."""
    monkeypatch.setattr(
        sys,
        "argv",
        ["shortcut-prefix-renamer", "--dry-run", str(tmp_path)],
    )
    main()
    captured = capsys.readouterr()
    assert "Dry run mode enabled" in captured.out


def test_accepts_shortcut_prefix_option(
    tmp_path: str,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test that the CLI accepts --shortcut-prefix option."""
    monkeypatch.setattr(
        sys,
        "argv",
        ["shortcut-prefix-renamer", str(tmp_path), "--shortcut-prefix", "Link to "],
    )
    main()  # Should not raise


def test_fails_without_directory_argument(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture,
) -> None:
    """Test that the CLI fails when no directory is provided."""
    monkeypatch.setattr(sys, "argv", ["shortcut-prefix-renamer"])
    with pytest.raises(SystemExit) as exc_info:
        main()
    assert exc_info.value.code != 0
    captured = capsys.readouterr()
    assert "the following arguments are required: directory" in captured.err.lower()


def test_fails_with_unknown_argument(
    tmp_path: str,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture,
) -> None:
    """Test that the CLI fails when an unknown argument is provided."""
    monkeypatch.setattr(
        sys,
        "argv",
        ["shortcut-prefix-renamer", "--unknown-flag", str(tmp_path)],
    )
    with pytest.raises(SystemExit) as exc_info:
        main()
    assert exc_info.value.code != 0
    captured = capsys.readouterr()
    assert "unrecognized arguments" in captured.err


@pytest.fixture
def dir_with_prefix_file(tmp_path: Path) -> Path:
    """Create a temporary directory with a Link to file."""
    prefix_file = tmp_path / "Link to Document.txt"
    prefix_file.write_text("This is a linked document.")
    return tmp_path


def test_renames_file_when_user_confirms_lowercase_y(
    dir_with_prefix_file: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture,
) -> None:
    """Test that file is renamed when user confirms."""
    monkeypatch.setattr(
        sys,
        "argv",
        ["shortcut-prefix-renamer", str(dir_with_prefix_file)],
    )
    monkeypatch.setattr("builtins.input", lambda _: "y")
    main()
    captured = capsys.readouterr()
    assert "Renamed" in captured.out
    assert not (dir_with_prefix_file / "Link to Document.txt").exists()
    assert (dir_with_prefix_file / "Document.txt").exists()


def test_renames_file_when_user_confirms_uppercase_y(
    dir_with_prefix_file: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture,
) -> None:
    """Test that file is renamed when user types 'Y'."""
    monkeypatch.setattr(
        sys,
        "argv",
        ["shortcut-prefix-renamer", str(dir_with_prefix_file)],
    )
    monkeypatch.setattr("builtins.input", lambda _: "Y")
    main()
    captured = capsys.readouterr()
    assert "Renamed" in captured.out
    assert not (dir_with_prefix_file / "Link to Document.txt").exists()
    assert (dir_with_prefix_file / "Document.txt").exists()


def test_renames_file_cancelled_when_user_types_n(
    dir_with_prefix_file: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture,
) -> None:
    """Test that file is not renamed when user types 'n'."""
    monkeypatch.setattr(
        sys,
        "argv",
        ["shortcut-prefix-renamer", str(dir_with_prefix_file)],
    )
    monkeypatch.setattr("builtins.input", lambda _: "n")
    main()
    captured = capsys.readouterr()
    assert "No files to rename" not in captured.out
    assert (dir_with_prefix_file / "Link to Document.txt").exists()
    assert not (dir_with_prefix_file / "Document.txt").exists()


def test_renames_file_cancelled_when_user_types_something_other_than_y(
    dir_with_prefix_file: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture,
) -> None:
    """Test that file is not renamed when user types 'n'."""
    monkeypatch.setattr(
        sys,
        "argv",
        ["shortcut-prefix-renamer", str(dir_with_prefix_file)],
    )
    monkeypatch.setattr("builtins.input", lambda _: "x")
    main()
    captured = capsys.readouterr()
    assert "No files to rename" not in captured.out
    assert (dir_with_prefix_file / "Link to Document.txt").exists()
    assert not (dir_with_prefix_file / "Document.txt").exists()


def test_renames_file_with_dry_run_when_user_confirms(
    dir_with_prefix_file: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture,
) -> None:
    """Test that file is not renamed in dry-run mode even when user confirms."""
    monkeypatch.setattr(
        sys,
        "argv",
        ["shortcut-prefix-renamer", "--dry-run", str(dir_with_prefix_file)],
    )
    monkeypatch.setattr("builtins.input", lambda _: "y")
    main()
    captured = capsys.readouterr()
    assert "Renamed" in captured.out
    assert (dir_with_prefix_file / "Link to Document.txt").exists()
    assert not (dir_with_prefix_file / "Document.txt").exists()


def test_sigint_handler_exits_gracefully(
    capsys: pytest.CaptureFixture,
) -> None:
    """Test that SIGINT (Ctrl+C) is handled gracefully."""
    with pytest.raises(SystemExit) as exc_info:
        os.kill(os.getpid(), signal.SIGINT)
    assert exc_info.value.code == 0
    captured = capsys.readouterr()
    assert "Operation cancelled by user" in captured.out


def test_sigint_during_input_exits_gracefully(
    dir_with_prefix_file: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture,
) -> None:
    """Test that SIGINT during input prompt is handled gracefully."""

    def raise_sigint(_prompt: str) -> str:
        os.kill(os.getpid(), signal.SIGINT)
        return ""  # This line won't be reached

    monkeypatch.setattr(
        sys,
        "argv",
        ["shortcut-prefix-renamer", str(dir_with_prefix_file)],
    )
    monkeypatch.setattr("builtins.input", raise_sigint)

    with pytest.raises(SystemExit) as exc_info:
        main()
    assert exc_info.value.code == 0
    captured = capsys.readouterr()
    assert "Operation cancelled by user" in captured.out
    # Verify venv was NOT deleted
    assert (dir_with_prefix_file / "Link to Document.txt").exists()
