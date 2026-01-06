"""Unit tests for utils (testing only the public interface)."""

from pathlib import Path

import pytest

from find_dups.utils import (
    DupFileReasonEnum,
    fail_if_invalid,
    find_potential_duplicates,
    format_duplicate_report,
    normalize_extensions,
)

# normalize_extensions tests


def test_normalize_extensions() -> None:
    """Test the normalize_extensions function."""
    input_extensions = ["txt", ".jpg", "png", ".md"]
    expected_output = [".txt", ".jpg", ".png", ".md"]
    assert normalize_extensions(input_extensions) == expected_output


def test_normalize_extensions_empty() -> None:
    """Test normalize_extensions with an empty list."""
    input_extensions = []
    expected_output = []
    assert normalize_extensions(input_extensions) == expected_output


# fail_if_invalid tests


def test_fail_if_invalid_nonexistent(tmp_path: Path) -> None:
    """Test fail_if_invalid with a nonexistent directory."""
    non_existent_path = tmp_path / "nonexistent"
    with pytest.raises(SystemExit) as exc_info:
        fail_if_invalid(non_existent_path)
    assert exc_info.value.code == 1


def test_fail_if_invalid_not_directory(tmp_path: Path) -> None:
    """Test fail_if_invalid with a path that is not a directory."""
    file_path = tmp_path / "file.txt"
    file_path.write_text("This is a test file.")
    with pytest.raises(SystemExit) as exc_info:
        fail_if_invalid(file_path)
    assert exc_info.value.code == 1


def test_fail_if_invalid_valid_directory(tmp_path: Path) -> None:
    """Test fail_if_invalid with a valid directory."""
    # This should not raise any exception
    fail_if_invalid(tmp_path)


# find_potential_duplicates tests
# scenarios:
# - trivial cases
#   - empty directory
#   - directory with no duplicates
# - directory with some duplicates (by size and hash, by name, by stem diff suffix)


def test_potential_duplicates_empty_dir(tmp_path: Path) -> None:
    """Test find_potential_duplicates with an empty directory."""
    duplicates = find_potential_duplicates(tmp_path)
    for reason in DupFileReasonEnum:
        assert duplicates[reason] == {}


def test_potential_duplicates_no_duplicates(tmp_path: Path) -> None:
    """Test find_potential_duplicates with a directory containing no duplicates."""
    # Create some unique files
    (tmp_path / "file1.txt").write_text("This is file 1.")
    (tmp_path / "file2.txt").write_text("This is file 2.")
    (tmp_path / "image1.jpg").write_text("This is image 1.")

    duplicates = find_potential_duplicates(tmp_path)
    for reason in DupFileReasonEnum:
        assert duplicates[reason] == {}


def test_potential_duplicates_with_duplicates(tmp_path: Path) -> None:
    """Test find_potential_duplicates with a directory containing duplicates."""
    # Create duplicate files by size and hash
    (tmp_path / "dup1.txt").write_text("Duplicate content.")
    (tmp_path / "dup2.txt").write_text("Duplicate content.")

    # Create duplicate files by name
    (tmp_path / "same_name.txt").write_text("Unique content 1.")
    (tmp_path / "subdir").mkdir()
    (tmp_path / "subdir" / "same_name.txt").write_text("Unique content 2.")

    # Create duplicate files by stem different suffix
    (tmp_path / "fileA.log").write_text("Log content.")
    (tmp_path / "fileA.txt").write_text("Text content.")

    duplicates = find_potential_duplicates(tmp_path)

    # Check duplicates by size and hash
    size_hash_dups = duplicates[DupFileReasonEnum.SAME_SIZE_AND_HASH]
    assert len(size_hash_dups) == 1
    assert set(size_hash_dups.popitem()[1]) == {
        tmp_path / "dup1.txt",
        tmp_path / "dup2.txt",
    }

    # Check duplicates by name
    name_dups = duplicates[DupFileReasonEnum.SAME_NAME]
    assert len(name_dups) == 1
    assert set(name_dups.popitem()[1]) == {
        tmp_path / "same_name.txt",
        tmp_path / "subdir" / "same_name.txt",
    }

    # Check duplicates by stem different suffix
    stem_dups = duplicates[DupFileReasonEnum.SAME_STEM_DIFF_SUFFIX]
    assert len(stem_dups) == 1
    assert set(stem_dups.popitem()[1]) == {
        tmp_path / "fileA.log",
        tmp_path / "fileA.txt",
    }


def test_potential_duplicates_with_extensions(tmp_path: Path) -> None:
    """Test find_potential_duplicates with extension filtering."""
    # Create files with different extensions
    (tmp_path / "file1.txt").write_text("Content A")
    (tmp_path / "file2.txt").write_text("Content A")  # Duplicate by content
    (tmp_path / "file3.jpg").write_text("Content B")
    (tmp_path / "file4.jpg").write_text("Content B")  # Duplicate by content
    (tmp_path / "file5.md").write_text("Content C")

    # Find duplicates only for .txt files
    duplicates_txt = find_potential_duplicates(tmp_path, extensions=[".txt"])
    size_hash_dups_txt = duplicates_txt[DupFileReasonEnum.SAME_SIZE_AND_HASH]
    assert len(size_hash_dups_txt) == 1
    assert set(size_hash_dups_txt.popitem()[1]) == {
        tmp_path / "file1.txt",
        tmp_path / "file2.txt",
    }

    # Find duplicates only for .jpg files
    duplicates_jpg = find_potential_duplicates(tmp_path, extensions=[".jpg"])
    size_hash_dups_jpg = duplicates_jpg[DupFileReasonEnum.SAME_SIZE_AND_HASH]
    assert len(size_hash_dups_jpg) == 1
    assert set(size_hash_dups_jpg.popitem()[1]) == {
        tmp_path / "file3.jpg",
        tmp_path / "file4.jpg",
    }


def test_potential_duplicates_hand_crafted(tmp_path: Path) -> None:
    """Test find_potential_duplicates with a hand-crafted scenario."""
    # Create directory structure with duplicates of different types
    # (the same structure and contents as in data/)
    # not sure about how stable the order is though, so this may be a flaky test,
    # but the results should be as the following:
    #     same hash:
    # "Content C":
    #   + file_3.out
    #   + subdir_2/file_21.out

    # "Content D":
    #   + some_file.txt
    #   + some_other_file.txt
    #   + yet_another_file.txt
    #   + subdir_1/yet_another_file.out
    #   + subdir_2/some_other_file.txt

    # "Content E":
    #   + subdir_1/file_11.txt
    #   + subdir_1/subdir_11/file_112.txt

    # same full name:
    # "some_file.txt":
    #   + some_file.txt
    #   + subdir_1/subdir_11/some_file.txt

    # + "some_other_file.txt":
    #   + some_other_file.txt
    #   + subdir2/some_other_file.txt

    # same stem, different suffix
    # "some_file":
    #   + some_file.txt
    #   + subdir_1/some_file.out

    # "yet_another_file":
    #   + yet_another_file.txt
    #   + subdir_1/yet_another_file.out
    (tmp_path / "file_1.txt").write_text("Content A")
    (tmp_path / "file_2.txt").write_text("Content B")
    (tmp_path / "file_3.out").write_text("Content C")
    (tmp_path / "some_file.txt").write_text("Content D")
    (tmp_path / "some_other_file.txt").write_text("Content D")
    (tmp_path / "yet_another_file.txt").write_text("Content D")

    (tmp_path / "subdir_1").mkdir()
    (tmp_path / "subdir_1" / "file_11.txt").write_text("Content E")
    (tmp_path / "subdir_1" / "file_12.txt").write_text("Content F")
    (tmp_path / "subdir_1" / "file_13.out").write_text("Content G")
    (tmp_path / "subdir_1" / "some_file.out").write_text("Content H")
    (tmp_path / "subdir_1" / "yet_another_file.out").write_text("Content D")

    (tmp_path / "subdir_1" / "subdir_11").mkdir()
    (tmp_path / "subdir_1" / "subdir_11" / "file_111.txt").write_text("Content I")
    (tmp_path / "subdir_1" / "subdir_11" / "file_112.txt").write_text("Content E")
    (tmp_path / "subdir_1" / "subdir_11" / "some_file.txt").write_text("Content J")

    (tmp_path / "subdir_2").mkdir()
    (tmp_path / "subdir_2" / "file_21.out").write_text("Content C")
    (tmp_path / "subdir_2" / "some_other_file.txt").write_text("Content D")

    duplicates = find_potential_duplicates(tmp_path)

    # Check duplicates by size and hash
    size_hash_dups = duplicates[DupFileReasonEnum.SAME_SIZE_AND_HASH]
    assert len(size_hash_dups) == 3  # noqa: PLR2004

    # Cotent E duplicates
    assert set(size_hash_dups.popitem()[1]) == {
        tmp_path / "subdir_1" / "file_11.txt",
        tmp_path / "subdir_1" / "subdir_11" / "file_112.txt",
    }

    # Content C duplicates
    assert set(size_hash_dups.popitem()[1]) == {
        tmp_path / "file_3.out",
        tmp_path / "subdir_2" / "file_21.out",
    }

    # Content D duplicates
    assert set(size_hash_dups.popitem()[1]) == {
        tmp_path / "some_other_file.txt",
        tmp_path / "some_file.txt",
        tmp_path / "yet_another_file.txt",
        tmp_path / "subdir_1" / "yet_another_file.out",
        tmp_path / "subdir_2" / "some_other_file.txt",
    }

    # Check duplicates by name
    name_dups = duplicates[DupFileReasonEnum.SAME_NAME]
    assert len(name_dups) == 2  # noqa: PLR2004

    # "some_file.txt" duplicates
    assert set(name_dups.popitem()[1]) == {
        tmp_path / "some_file.txt",
        tmp_path / "subdir_1" / "subdir_11" / "some_file.txt",
    }

    # "some_other_file.txt" duplicates
    assert set(name_dups.popitem()[1]) == {
        tmp_path / "some_other_file.txt",
        tmp_path / "subdir_2" / "some_other_file.txt",
    }

    # Check duplicates by stem different suffix
    stem_dups = duplicates[DupFileReasonEnum.SAME_STEM_DIFF_SUFFIX]
    assert len(stem_dups) == 2  # noqa: PLR2004

    # "yet_another_file" stem duplicates
    assert set(stem_dups.popitem()[1]) == {
        tmp_path / "yet_another_file.txt",
        tmp_path / "subdir_1" / "yet_another_file.out",
    }

    # "some_file" stem duplicates
    assert set(stem_dups.popitem()[1]) == {
        tmp_path / "some_file.txt",
        tmp_path / "subdir_1" / "some_file.out",
    }


def test_format_duplicate_report_empty() -> None:
    """Test format_duplicate_report with no duplicates."""
    duplicates: dict[DupFileReasonEnum, dict[str, list[Path]]] = {
        DupFileReasonEnum.SAME_SIZE_AND_HASH: {},
        DupFileReasonEnum.SAME_NAME: {},
        DupFileReasonEnum.SAME_STEM_DIFF_SUFFIX: {},
    }
    report = format_duplicate_report(duplicates)
    assert report == "\n".join(  # noqa: FLY002
        [
            "Reason: same size and hash",
            "    No potential duplicates found.\n",
            "Reason: same name",
            "    No potential duplicates found.\n",
            "Reason: same stem different suffix",
            "    No potential duplicates found.\n",
        ],
    )


def test_format_duplicate_report_with_duplicates() -> None:
    """Test format_duplicate_report with some duplicates."""
    duplicates: dict[DupFileReasonEnum, dict[str, list[Path]]] = {
        DupFileReasonEnum.SAME_SIZE_AND_HASH: {
            "duplicate_group_1": [
                Path("dup1.txt"),
                Path("dup2.txt"),
            ],
        },
        DupFileReasonEnum.SAME_NAME: {
            "some_name_group": [
                Path("some_name.txt"),
                Path("another_same_name.txt"),
            ],
        },
        DupFileReasonEnum.SAME_STEM_DIFF_SUFFIX: {
            "some_stem_group": [
                Path("file1.log"),
                Path("file1.txt"),
                Path("file1.md"),
            ],
        },
    }
    report = format_duplicate_report(duplicates)

    expected_lines = [
        "Reason: same size and hash",
        "    - dup1.txt",
        "    - dup2.txt",
        "",
        "",
        "Reason: same name",
        "    - some_name.txt",
        "    - another_same_name.txt",
        "",
        "",
        "Reason: same stem different suffix",
        "    - file1.log",
        "    - file1.txt",
        "    - file1.md",
        "",
        "",
    ]

    assert report == "\n".join(expected_lines)
