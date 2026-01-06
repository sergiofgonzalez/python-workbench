"""Unit tests for main (end-to-end testing)."""

import os
import signal
import sys
from pathlib import Path

import pytest

from purge_venv.main import main


def test_accepts_directory_argument(
    tmp_path: str,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture,
) -> None:
    """Test that the CLI accepts a directory argument."""
    monkeypatch.setattr(sys, "argv", ["purge-venv", str(tmp_path)])
    main()
    captured = capsys.readouterr()
    assert "No virtual environment directories found" in captured.out


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


def test_fails_without_directory_argument(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture,
) -> None:
    """Test that the CLI fails when no directory is provided."""
    monkeypatch.setattr(sys, "argv", ["purge-venv"])
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
        ["purge-venv", "--unknown-flag", str(tmp_path)],
    )
    with pytest.raises(SystemExit) as exc_info:
        main()
    assert exc_info.value.code != 0
    captured = capsys.readouterr()
    assert "unrecognized arguments" in captured.err


@pytest.fixture
def dir_with_venv(tmp_path: Path) -> Path:
    """Create a temporary directory with a .venv subdirectory."""
    venv_dir = tmp_path / ".venv"
    venv_dir.mkdir()
    # Add a file inside to make it non-empty
    (venv_dir / "pyvenv.cfg").write_text("home = /usr/bin/python3")
    return tmp_path


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


def test_deletes_venv_when_user_confirms_with_uppercase_y(
    dir_with_venv: Path,  # custom fixture
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture,
) -> None:
    """Test that venv is deleted when user types 'Y'."""
    monkeypatch.setattr(sys, "argv", ["purge-venv", str(dir_with_venv)])
    monkeypatch.setattr("builtins.input", lambda _: "Y")
    main()
    captured = capsys.readouterr()
    assert "Purge complete" in captured.out
    assert not (dir_with_venv / ".venv").exists()


def test_cancels_when_user_types_n(
    dir_with_venv: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture,
) -> None:
    """Test that purge is cancelled when user types 'n'."""
    monkeypatch.setattr(sys, "argv", ["purge-venv", str(dir_with_venv)])
    monkeypatch.setattr("builtins.input", lambda _: "n")
    main()
    captured = capsys.readouterr()
    assert "Purge cancelled by user" in captured.out
    assert (dir_with_venv / ".venv").exists()


def test_cancels_when_user_types_anything_other_than_y(
    dir_with_venv: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture,
) -> None:
    """Test that purge is cancelled for any input other than y/Y."""
    monkeypatch.setattr(sys, "argv", ["purge-venv", str(dir_with_venv)])
    monkeypatch.setattr("builtins.input", lambda _: "maybe")
    main()
    captured = capsys.readouterr()
    assert "Purge cancelled by user" in captured.out
    assert (dir_with_venv / ".venv").exists()


def test_cancels_when_user_presses_enter(
    dir_with_venv: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture,
) -> None:
    """Test that purge is cancelled when user just presses Enter."""
    monkeypatch.setattr(sys, "argv", ["purge-venv", str(dir_with_venv)])
    monkeypatch.setattr("builtins.input", lambda _: "")
    main()
    captured = capsys.readouterr()
    assert "Purge cancelled by user" in captured.out
    assert (dir_with_venv / ".venv").exists()


def test_dry_run_does_not_delete_venv_when_user_confirms(
    dir_with_venv: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture,
) -> None:
    """Test that --dry-run prevents deletion even when user confirms."""
    monkeypatch.setattr(
        sys,
        "argv",
        ["purge-venv", "--dry-run", str(dir_with_venv)],
    )
    monkeypatch.setattr("builtins.input", lambda _: "y")
    main()
    captured = capsys.readouterr()
    assert "Dry run complete" in captured.out
    assert (dir_with_venv / ".venv").exists()


def test_dry_run_shows_what_would_be_deleted(
    dir_with_venv: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture,
) -> None:
    """Test that --dry-run shows which directories would be deleted."""
    monkeypatch.setattr(
        sys,
        "argv",
        ["purge-venv", "--dry-run", str(dir_with_venv)],
    )
    monkeypatch.setattr("builtins.input", lambda _: "y")
    main()
    captured = capsys.readouterr()
    assert ".venv" in captured.out
    assert "No directories were deleted" in captured.out
    assert (dir_with_venv / ".venv").exists()


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
    dir_with_venv: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture,
) -> None:
    """Test that SIGINT during input prompt is handled gracefully."""

    def raise_sigint(_prompt: str) -> str:
        os.kill(os.getpid(), signal.SIGINT)
        return ""  # This line won't be reached

    monkeypatch.setattr(sys, "argv", ["purge-venv", str(dir_with_venv)])
    monkeypatch.setattr("builtins.input", raise_sigint)

    with pytest.raises(SystemExit) as exc_info:
        main()
    assert exc_info.value.code == 0
    captured = capsys.readouterr()
    assert "Operation cancelled by user" in captured.out
    # Verify venv was NOT deleted
    assert (dir_with_venv / ".venv").exists()
