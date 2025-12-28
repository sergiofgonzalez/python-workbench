"""Illustrates how to rename and move files using pathlib rename and unline."""

from pathlib import Path

tmp_dir = Path("data") / "out_data" / "tmp"


def setup() -> None:
    """Set everything up to demonstrate renaming and moving files."""
    log_file = tmp_dir / "app.log"
    log_file.touch(exist_ok=True)
    archive_dir = tmp_dir / "archive"
    archive_dir.mkdir(exist_ok=True)


def teardown() -> None:
    """Clean up after the demonstration."""
    log_file = tmp_dir / "app.log"
    if log_file.exists():
        log_file.unlink()
    archive_dir = tmp_dir / "archive"
    if archive_dir.exists():
        for item in archive_dir.iterdir():
            item.unlink()
        archive_dir.rmdir()


def main() -> None:
    """Application entry point."""
    setup()
    # Rename an existing file on its own path
    log_file = tmp_dir / "app.log"
    if log_file.exists():
        new_log_file = tmp_dir / "app.log.old"
        print(f"Renaming file: {log_file} to {new_log_file}")
        assert not new_log_file.exists()
        log_file.rename(new_log_file)
        assert new_log_file.exists()
        assert not log_file.exists()
    print("=== passed renaming test ===")

    # Renaming (moving) a file to a different directory
    archive_dir = tmp_dir / "archive"
    if new_log_file.exists():
        moved_log_file = archive_dir / "app.log.old"
        print(f"Moving file: {new_log_file} to {moved_log_file}")
        assert not moved_log_file.exists()
        new_log_file.rename(moved_log_file)
        assert moved_log_file.exists()
        assert not new_log_file.exists()
    print("=== passed moving test ===")

    # Delete the moved file to clean up
    if moved_log_file.exists():
        moved_log_file.unlink()
        print(f"Deleted file: {moved_log_file}")
        assert not moved_log_file.exists()
    print("=== cleanup completed ===")

    # Confirm the archive directory is empty
    if archive_dir.exists():
        assert not any(archive_dir.iterdir())
        print(f"Archive directory {archive_dir} is empty.")
    # ... and yet you cannot remove it with unlink()
    try:
        archive_dir.unlink()  # This will raise an exception
    except IsADirectoryError as e:
        print(f"Cannot remove directory with unlink(): {e}")
    print("=== passed directory unlink test ===")
    teardown()


if __name__ == "__main__":
    main()
