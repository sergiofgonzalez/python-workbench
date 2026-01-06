"""Unit tests for utils (testing only the public interface)."""

from pathlib import Path

import pytest

from purge_venv.utils import (
    delete_dirs,
    fail_if_not_valid_root_dir,
    fail_if_too_many_venv_names,
    find_venv_dirs,
    report_dir_size_before_after_purge,
    report_purge_completion,
    report_venvs_found,
)


def test_delete_dirs_happy_path(tmp_path: Path) -> None:
    """Test deleting directories."""
    dir_to_delete = tmp_path / "venv_to_delete"
    dir_to_delete.mkdir()
    (dir_to_delete / "file.txt").write_text("test")
    subdir = dir_to_delete / "subdir"
    subdir.mkdir()
    (subdir / "subfile.txt").write_text("subtest")

    err_messages = delete_dirs([dir_to_delete])
    assert not err_messages
    assert not dir_to_delete.exists()


def test_delete_dirs_non_existent(tmp_path: Path) -> None:
    """Test deleting a non-existent directory."""
    non_existent_dir = tmp_path / "non_existent_venv"

    err_messages = delete_dirs([non_existent_dir])
    assert len(err_messages) == 1
    assert "No such file or directory" in err_messages[0]


def test_fail_if_not_valid_root_dir_non_existent_dir(tmp_path: Path) -> None:
    """Test that no exception is raised for a valid root directory."""
    non_existent_dir = tmp_path / "non_existent_dir"

    # This should not raise an exception
    with pytest.raises(SystemExit):
        fail_if_not_valid_root_dir(non_existent_dir)


def test_fail_if_not_valid_root_dir_not_a_directory(tmp_path: Path) -> None:
    """Test that an exception is raised for a path that is not a directory."""
    file_path = tmp_path / "not_a_directory.txt"
    file_path.write_text("I am a file, not a directory.")

    with pytest.raises(SystemExit):
        fail_if_not_valid_root_dir(file_path)


def test_fail_if_not_valid_root_dir_valid_directory(tmp_path: Path) -> None:
    """Test that no exception is raised for a valid root directory."""
    valid_dir = tmp_path / "valid_directory"
    valid_dir.mkdir()

    # This should not raise an exception
    fail_if_not_valid_root_dir(valid_dir)


def test_fail_if_too_many_venv_names() -> None:
    """Test that an exception is raised when too many venv names are provided."""
    venv_names = ["venv1", "venv2", "venv3", "venv4", "venv5", "venv6"]

    with pytest.raises(SystemExit):
        fail_if_too_many_venv_names(venv_names)


def test_fail_if_too_many_venv_names_within_limit() -> None:
    """Test no exception is raised when the number of venv names is within the limit."""
    venv_names = ["venv1", "venv2", "venv3"]

    # This should not raise an exception
    fail_if_too_many_venv_names(venv_names)


def test_fail_if_too_many_venv_names_at_limit() -> None:
    """Test no exception is raised when the number of venv names is at the limit."""
    venv_names = ["venv1", "venv2", "venv3", "venv4", "venv5"]

    # This should not raise an exception
    fail_if_too_many_venv_names(venv_names)


def test_fail_if_too_many_venv_names_empty_list() -> None:
    """Test that no exception is raised when the venv names list is empty."""
    venv_names = []

    # This should not raise an exception
    fail_if_too_many_venv_names(venv_names)


def test_find_venv_dirs_no_venvs_empty_dir(tmp_path: Path) -> None:
    """Test finding venv dirs when none exist."""
    found_dirs = find_venv_dirs(tmp_path, ["venv", ".venv"])
    assert found_dirs == []


def test_find_venv_dirs_no_venvs_non_empty_dir(tmp_path: Path) -> None:
    """Test finding venv dirs when none exist in a non-empty directory."""
    (tmp_path / "some_file.txt").write_text("Just a file.")
    (tmp_path / "another_dir").mkdir()

    found_dirs = find_venv_dirs(tmp_path, ["venv", ".venv"])
    assert found_dirs == []


def test_find_venv_dirs_multiple_venvs(tmp_path: Path) -> None:
    """Test finding multiple venv dirs."""
    venv1 = tmp_path / "venv"
    venv1.mkdir()
    venv2 = tmp_path / "project" / ".venv"
    venv2.parent.mkdir()
    venv2.mkdir()
    venv3 = tmp_path / "another_project" / "venv"
    venv3.parent.mkdir()
    venv3.mkdir()

    found_dirs = find_venv_dirs(tmp_path, ["venv", ".venv"])
    assert found_dirs == sorted([venv1, venv2, venv3])


def test_find_venv_dirs_nested_venvs(tmp_path: Path) -> None:
    """Test finding nested venv dirs."""
    venv1 = tmp_path / "venv"
    venv1.mkdir()
    venv2 = venv1 / "nested" / ".venv"
    venv2.parent.mkdir()
    venv2.mkdir()

    found_dirs = find_venv_dirs(tmp_path, ["venv", ".venv"])
    assert found_dirs == sorted([venv1, venv2])


def test_find_venv_dirs_similar_names(tmp_path: Path) -> None:
    """Test finding venv dirs with similar names."""
    venv = tmp_path / "venv"
    venv.mkdir()
    not_venv = tmp_path / "venv_backup"
    not_venv.mkdir()
    another_not_venv = tmp_path / "venv1"
    another_not_venv.mkdir()
    yet_another_not_venv = tmp_path / ".venv"
    yet_another_not_venv.mkdir()

    found_dirs = find_venv_dirs(tmp_path, ["venv"])
    assert found_dirs == [venv]


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


def test_report_dir_size_large_file(
    capsys: pytest.CaptureFixture,
    tmp_path: Path,
) -> None:
    """Test reporting directory size with a large file."""
    venv_dir = tmp_path / "venv"
    venv_dir.mkdir()
    (venv_dir / "large_file.bin").write_bytes(b"a" * 5_242_880)  # 5 MB

    report_dir_size_before_after_purge(venv_dir, before=True)
    captured = capsys.readouterr()
    assert "before purge: 5.00 MB" in captured.out


def test_report_purge_completion_happy_path(
    capsys: pytest.CaptureFixture,
    tmp_path: Path,
) -> None:
    """Test reporting purge completion."""
    venv_dir = tmp_path / "venv"
    venv_dir.mkdir()
    (venv_dir / "file1.txt").write_text("a" * 100)  # 100 bytes

    report_purge_completion([])
    captured = capsys.readouterr()
    assert "Purge completed successfully without errors." in captured.out


def test_report_purge_completion_with_errors(
    capsys: pytest.CaptureFixture,
    tmp_path: Path,
) -> None:
    """Test reporting purge completion with errors."""
    venv_dir = tmp_path / "venv"
    venv_dir.mkdir()
    (venv_dir / "file1.txt").write_text("a" * 100)  # 100 bytes

    error_messages = ["Error1", "Error2"]
    report_purge_completion(error_messages)
    captured = capsys.readouterr()
    assert "Purge completed with errors:" in captured.out
    assert "Some errors occurred during deletion:" in captured.out
    assert f"- {error_messages[0]}" in captured.out
    assert f"- {error_messages[1]}" in captured.out


def test_report_venvs_found_no_venvs(
    capsys: pytest.CaptureFixture,
    tmp_path: Path,
) -> None:
    """Test reporting when no venvs are found."""
    report_venvs_found(tmp_path, [], ["venv", ".venv"])
    captured = capsys.readouterr()
    assert "No virtual environment directories found" in captured.out


def test_report_venvs_found_with_venvs(
    capsys: pytest.CaptureFixture,
    tmp_path: Path,
) -> None:
    """Test reporting when venvs are found."""
    venv1 = tmp_path / "venv"
    venv1.mkdir()
    (venv1 / "file1.txt").write_text("a" * 150)  # 150 bytes
    venv2 = tmp_path / "project" / ".venv"
    venv2.parent.mkdir()
    venv2.mkdir()
    (venv2 / "file2.txt").write_text("b" * 250)  # 250 bytes

    report_venvs_found(tmp_path, [venv1, venv2], ["venv", ".venv"])
    captured = capsys.readouterr()
    assert "Found 2 virtual environment directories" in captured.out
    assert "- venv: 150.00 B" in captured.out
    assert "- project/.venv: 250.00 B" in captured.out
    assert "(Total size: 400.00 B)" in captured.out
