"""Unit tests for utils (testing only the public interface)."""

from pathlib import Path

import pytest

from shortcut_prefix_renamer.utils import (
    fail_if_not_valid_root_dir,
    find_files_with_prefix,
    rename_files,
    report_files_with_prefix_found,
    report_rename_completion,
)


def test_fail_if_not_valid_root_dir_nonexistent(tmp_path: Path) -> None:
    """Test fail_if_not_valid_root_dir with a nonexistent directory."""
    non_existent_path = tmp_path / "nonexistent"
    with pytest.raises(SystemExit):
        fail_if_not_valid_root_dir(non_existent_path)


def test_fail_if_not_valid_root_dir_not_directory(tmp_path: Path) -> None:
    """Test fail_if_not_valid_root_dir with a path that is not a directory."""
    file_path = tmp_path / "file.txt"
    file_path.write_text("This is a test file.")
    with pytest.raises(SystemExit):
        fail_if_not_valid_root_dir(file_path)


def test_fail_if_not_valid_root_dir_valid_directory(tmp_path: Path) -> None:
    """Test fail_if_not_valid_root_dir with a valid directory."""
    # This should not raise any exception
    fail_if_not_valid_root_dir(tmp_path)


def test_find_files_with_prefix_no_files(tmp_path: Path) -> None:
    """Test find_files_with_prefix when no files match the prefix."""
    prefix = "Link to "
    found_files = find_files_with_prefix(tmp_path, prefix)
    assert found_files == []


def test_find_files_with_prefix_some_files(tmp_path: Path) -> None:
    """Test find_files_with_prefix when some files match the prefix."""
    prefix = "Link to "
    matching_file = tmp_path / "Link to Document.txt"
    non_matching_file = tmp_path / "Document.txt"
    matching_file.write_text("This is a linked document.")
    non_matching_file.write_text("This is a regular document.")

    found_files = find_files_with_prefix(tmp_path, prefix)
    assert found_files == [matching_file]


def test_find_files_with_prefix_nested_files(tmp_path: Path) -> None:
    """Test find_files_with_prefix with nested directories."""
    prefix = "Link to "
    nested_dir = tmp_path / "nested"
    nested_dir.mkdir()
    matching_file = nested_dir / "Link to Nested Document.txt"
    non_matching_file = nested_dir / "Nested Document.txt"
    matching_file.write_text("This is a linked nested document.")
    non_matching_file.write_text("This is a regular nested document.")

    found_files = find_files_with_prefix(tmp_path, prefix)
    assert found_files == [matching_file]


def test_find_files_with_prefix_multiple_matches(tmp_path: Path) -> None:
    """Test find_files_with_prefix with multiple matching files."""
    prefix = "Link to "
    matching_file1 = tmp_path / "Link to Document1.txt"
    matching_file2 = tmp_path / "Link to Document2.txt"
    matching_file1.write_text("This is linked document 1.")
    matching_file2.write_text("This is linked document 2.")

    found_files = find_files_with_prefix(tmp_path, prefix)
    assert set(found_files) == {matching_file1, matching_file2}


def test_find_files_with_prefix_different_prefix(tmp_path: Path) -> None:
    """Test find_files_with_prefix with a different prefix."""
    prefix = "Shortcut to "
    matching_file = tmp_path / "Shortcut to Document.txt"
    non_matching_file = tmp_path / "Link to Document.txt"
    matching_file.write_text("This is a shortcut document.")
    non_matching_file.write_text("This is a linked document.")

    found_files = find_files_with_prefix(tmp_path, prefix)
    assert found_files == [matching_file]


def test_rename_files_noop(tmp_path: Path) -> None:
    """Test rename_files in dry-run mode (no actual renaming)."""
    prefix = "Link to "
    matching_file = tmp_path / "Link to Document.txt"
    matching_file.write_text("This is a linked document.")

    found_files = [matching_file]
    status_messages = rename_files(found_files, prefix, dry_run=True)

    assert len(status_messages) == 1
    assert matching_file.exists()  # File should still exist with original name


def test_rename_files_actual_rename(tmp_path: Path) -> None:
    """Test rename_files with actual renaming."""
    prefix = "Link to "
    matching_file = tmp_path / "Link to Document.txt"
    matching_file.write_text("This is a linked document.")

    found_files = [matching_file]
    status_messages = rename_files(found_files, prefix, dry_run=False)

    expected_new_file = tmp_path / "Document.txt"
    assert len(status_messages) == 1
    assert not matching_file.exists()  # Original file should not exist
    assert expected_new_file.exists()  # New file should exist


def test_rename_files_name_collision(tmp_path: Path) -> None:
    """Test rename_files handling name collisions."""
    prefix = "Link to "
    matching_file = tmp_path / "Link to Document.txt"
    existing_file = tmp_path / "Document.txt"

    matching_file.write_text("This is linked document 1.")
    existing_file.write_text("This is an existing document.")

    found_files = [matching_file]
    status_messages = rename_files(found_files, prefix, dry_run=False)

    expected_new_file = tmp_path / "Document_001.txt"

    assert len(status_messages) == 1
    assert not matching_file.exists()  # Original file 1 should not exist
    assert expected_new_file.exists()  # New file should exist


def test_rename_files_name_collision_failed(tmp_path: Path) -> None:
    """Test rename_files handling name collisions."""
    prefix = "Link to "
    matching_file = tmp_path / "Link to Document.txt"
    existing_file = tmp_path / "Document.txt"
    matching_file.write_text("This is linked document.")
    existing_file.write_text("This is an existing document.")

    for i in range(1, 1000):
        collision_file = tmp_path / f"Document_{i:03d}.txt"
        collision_file.write_text("This is a colliding document.")

    found_files = [matching_file]
    status_messages = rename_files(found_files, prefix, dry_run=False)

    assert len(status_messages) == 1
    assert "could not find a unique name after 999 attempts" in status_messages[0]
    assert matching_file.exists()  # Original file should still exist
    assert existing_file.exists()  # Existing file should still exist


def test_rename_files_multiple(tmp_path: Path) -> None:
    """Test rename_files with multiple files to rename."""
    prefix = "Link to "
    matching_file1 = tmp_path / "Link to Document1.txt"
    matching_file2 = tmp_path / "Link to Document2.txt"
    matching_file1.write_text("This is linked document 1.")
    matching_file2.write_text("This is linked document 2.")

    found_files = [matching_file1, matching_file2]
    status_messages = rename_files(found_files, prefix, dry_run=False)

    expected_new_file1 = tmp_path / "Document1.txt"
    expected_new_file2 = tmp_path / "Document2.txt"

    assert len(status_messages) == 2  # noqa: PLR2004
    assert not matching_file1.exists()  # Original file 1 should not exist
    assert not matching_file2.exists()  # Original file 2 should not exist
    assert expected_new_file1.exists()  # New file 1 should exist
    assert expected_new_file2.exists()  # New file 2 should exist


def test_report_files_with_prefix_found_empty(
    capsys: pytest.CaptureFixture,
    tmp_path: Path,
) -> None:
    """Test report_files_with_prefix_found with no files found."""
    prefix = "Link to "
    report_files_with_prefix_found(tmp_path, [], prefix)

    captured = capsys.readouterr()
    assert f"No files found with prefix '{prefix}' within " in captured.out


def test_report_files_with_prefix_found_some(
    capsys: pytest.CaptureFixture,
    tmp_path: Path,
) -> None:
    """Test report_files_with_prefix_found with some files found."""
    prefix = "Link to "
    matching_file1 = tmp_path / "Link to Document1.txt"
    matching_file2 = tmp_path / "Link to Document2.txt"
    matching_file1.write_text("This is linked document 1.")
    matching_file2.write_text("This is linked document 2.")

    found_files = [matching_file1, matching_file2]
    report_files_with_prefix_found(tmp_path, found_files, prefix)

    captured = capsys.readouterr()
    assert f"Found 2 files starting with prefix '{prefix}' within " in captured.out
    assert f"- {matching_file1.relative_to(tmp_path)}" in captured.out
    assert f"- {matching_file2.relative_to(tmp_path)}" in captured.out


def test_report_files_with_prefix_found_single(
    capsys: pytest.CaptureFixture,
    tmp_path: Path,
) -> None:
    """Test report_files_with_prefix_found with a single file found."""
    prefix = "Link to "
    matching_file = tmp_path / "Link to Document.txt"
    matching_file.write_text("This is a linked document.")

    found_files = [matching_file]
    report_files_with_prefix_found(tmp_path, found_files, prefix)

    captured = capsys.readouterr()
    assert f"Found 1 file starting with prefix '{prefix}' within " in captured.out
    assert f"- {matching_file.relative_to(tmp_path)}" in captured.out


def test_report_rename_completion(capsys: pytest.CaptureFixture) -> None:
    """Test report_rename_completion function."""
    status_messages = [
        "Renamed: /path/to/Link to Document1.txt -> /path/to/Document1.txt",
        "Renamed: /path/to/Link to Document2.txt -> /path/to/Document2.txt",
    ]
    report_rename_completion(status_messages)

    captured = capsys.readouterr()
    for message in status_messages:
        assert message in captured.out
