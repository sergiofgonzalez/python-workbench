"""Illustrate different features of pathlib related to file information."""

from pathlib import Path


def main() -> None:
    """Application entry point."""
    # Path.exists(): Check if a path exists
    path = Path("427_pathlib_info_about_files.py")
    assert path.exists()  # The file should exist

    path = Path("non_existent_file.txt")
    assert not path.exists()  # The file should not exist
    print("==" * 40)

    # Path.isdir() and Path.is_file(): Check if a path is a directory or a file
    dir_path = Path()  # Current directory
    assert dir_path.is_dir()  # Should be a directory
    assert not dir_path.is_file()  # Should not be a file

    file_path = Path("427_pathlib_info_about_files.py")
    assert file_path.is_file()  # Should be a file
    assert not file_path.is_dir()  # Should not be a directory
    print("==" * 40)

    # Path.is_symlink(): Check if a path is a symbolic link
    symlink_path = Path("~") / "win_downloads"
    assert symlink_path.expanduser().is_symlink()
    print("==" * 40)

    # Path.is_mount(): Check if a path is a mount point
    mount_path = Path("/mnt/c")
    assert mount_path.is_mount()
    print("==" * 40)

    # Path.samefile(): Check if two paths point to the same file
    path1 = Path("427_pathlib_info_about_files.py")
    path2 = Path("./427_pathlib_info_about_files.py")
    assert path1.samefile(path2)
    print("==" * 40)

    # Path.isabsolute(): Check if a path is absolute
    abs_path = Path("/usr/bin/python3")
    rel_path = Path("some/relative/path.txt")
    assert abs_path.is_absolute()
    assert not rel_path.is_absolute()

    abs_win_path = Path("C:\\Windows\\System32")
    rel_win_path = Path("Documents\\file.txt")
    try:
        assert abs_win_path.is_absolute()
    except AssertionError:
        print("One of the assertions failed for Windows paths.")
    assert not rel_win_path.is_absolute()
    print("==" * 40)

    # Path.stat(): Get detailed information about a file
    file_stat = Path("427_pathlib_info_about_files.py").stat()
    print(f"File size: {file_stat.st_size} bytes")
    print(f"Last modified time: {file_stat.st_mtime}")
    print(f"Last accessed time: {file_stat.st_atime}")
    print(f"Creation time: {file_stat.st_ctime}")
    print(f"File mode: {file_stat.st_mode:o}")
    print("==" * 40)


if __name__ == "__main__":
    main()
