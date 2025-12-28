"""Illustrates how to create and delete directories using pathlib mkdir and rmdir."""

import shutil
from pathlib import Path


def teardown() -> None:
    """Clean up after the demonstration."""
    new_dir = Path("data") / "out_data" / "new_directory"
    if new_dir.exists() and new_dir.is_dir():
        shutil.rmtree(new_dir)
        print(f"Deleted directory: {new_dir}")
        assert not new_dir.exists()
    nested_dir = Path("data") / "out_data" / "nested"
    if nested_dir.exists() and nested_dir.is_dir():
        shutil.rmtree(nested_dir)
        print(f"Deleted directory: {nested_dir}")
        assert not nested_dir.exists()
    print("=== cleanup completed ===")


def main() -> None:
    """Application entry point."""
    # Create a new directory
    new_dir = Path("data") / "out_data" / "new_directory"
    new_dir.mkdir(exist_ok=True)
    print(f"Created directory: {new_dir}")
    assert new_dir.exists()
    assert new_dir.is_dir()
    print("=" * 40)

    # Create a nested directory structure
    nested_dir = Path("data") / "out_data" / "nested" / "dir" / "structure"
    nested_dir.mkdir(parents=True, exist_ok=True)
    print(f"Created nested directory structure: {nested_dir}")
    assert nested_dir.exists()
    assert nested_dir.is_dir()
    print("=" * 40)

    # Removing empty directories with rmdir()
    try:
        new_dir.rmdir()
        print(f"Deleted directory: {new_dir}")
        assert not new_dir.exists()
    except OSError as e:
        print(f"Error deleting directory {new_dir}: {e}")
    print("=== passed non-empty directory deletion test ===")

    # Removing empty directories in nested structure
    nested_dir.rmdir()  # removes 'structure'
    print(f"Deleted directory: {nested_dir}")
    parent_dir = nested_dir.parent  # 'dir'
    parent_dir.rmdir()  # removes 'dir'
    print(f"Deleted directory: {parent_dir}")
    grandparent_dir = parent_dir.parent  # 'nested'
    grandparent_dir.rmdir()  # removes 'nested'
    print(f"Deleted directory: {grandparent_dir}")
    assert not grandparent_dir.exists()
    print("=== passed nested directory deletion test ===")

    teardown()


if __name__ == "__main__":
    main()
