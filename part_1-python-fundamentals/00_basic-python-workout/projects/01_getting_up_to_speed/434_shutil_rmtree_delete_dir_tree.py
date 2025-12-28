"""Illustrate how to delete entire directory trees with shutil.rmtree()."""

import shutil
from pathlib import Path


def main() -> None:
    """Application entry point."""
    # Create a sample directory tree for demonstration
    base_dir = Path("data") / "out_data" / "sample_tree"
    (base_dir / "subdir1").mkdir(parents=True, exist_ok=True)
    (base_dir / "subdir2").mkdir(parents=True, exist_ok=True)
    (base_dir / "subdir1" / "file1.txt").touch()
    (base_dir / "subdir2" / "file2.txt").touch()
    print(f"Created sample directory tree at: {base_dir}")
    print("=" * 40)

    # Now delete the entire directory tree
    shutil.rmtree(base_dir)
    print(f"Deleted directory tree at: {base_dir}")
    assert not base_dir.exists()
    print("=== passed directory tree deletion test ===")


if __name__ == "__main__":
    main()
