"""Illustrate how to copy entire directory trees with shutil.copytree()."""

import shutil
from pathlib import Path


def setup_and_teardown() -> None:
    """Set up a sample directory tree for demonstration."""
    shutil.rmtree(Path("data") / "out_data" / "tmp" / "copied_tree", ignore_errors=True)


def main() -> None:
    """Application entry point."""
    setup_and_teardown()

    in_data = Path("data") / "in_data"
    out_data = Path("data") / "out_data" / "tmp" / "copied_tree"

    # Ensure the output directory does not already exist
    if out_data.exists():
        shutil.rmtree(out_data)
    # Copy the entire directory tree
    shutil.copytree(in_data, out_data)
    print(f"Copied directory tree from {in_data} to {out_data}")
    assert out_data.exists()

    # Let's verify that the contents were copied
    for root, dirs, files in in_data.walk():
        relative_root = Path(root).relative_to(in_data)
        corresponding_root = out_data / relative_root
        for dir_name in dirs:
            dir_path = corresponding_root / dir_name
            assert dir_path.exists()
            assert dir_path.is_dir()
        for file_name in files:
            file_path = corresponding_root / file_name
            orig_stat = (Path(root) / file_name).stat()
            copied_stat = file_path.stat()
            assert file_path.exists()
            assert file_path.is_file()
            assert orig_stat.st_size == copied_stat.st_size
            assert orig_stat.st_mtime == copied_stat.st_mtime
            # this is updated: assert orig_stat.st_ctime == copied_stat.st_ctime
            assert orig_stat.st_atime == copied_stat.st_atime
            assert orig_stat.st_mode == copied_stat.st_mode
            print(f"Verified file: {file_name}")
    print("=== passed directory tree copy test ===")
    setup_and_teardown()


if __name__ == "__main__":
    main()
