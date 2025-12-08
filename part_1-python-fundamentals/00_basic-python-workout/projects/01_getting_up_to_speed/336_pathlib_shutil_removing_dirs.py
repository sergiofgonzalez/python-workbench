"""Illustrates removing directories using shutil.rmtree and pathlib.Path.rmdir."""

import shutil
from pathlib import Path

in_dir_path = Path("data/in_data/my_files")
dst_dir_path = Path("data/out_data/tmp/moved_files")


def main() -> None:
    """Application entry point."""
    # We first make a mirror of the input directory to remove directories from
    shutil.copytree(in_dir_path, dst_dir_path, dirs_exist_ok=True)

    # Now we remove directories from the destination directory
    # Path.rmdir can only remove empty directories
    try:
        print(f"Removing directory {dst_dir_path} using rmdir")
        dst_dir_path.rmdir()
    except OSError as e:
        print(
            f"Error removing directory {dst_dir_path} using rmdir: "
            f"{e} (type: {type(e).__name__})",
        )
    print("=== Passed 1 ===")

    # shutil.rmtree can remove non-empty directories
    print(f"Removing directory {dst_dir_path} using shutil.rmtree")
    shutil.rmtree(dst_dir_path)
    print("=== Passed 2 ===")

    # Now we create an empty directory and remove it using Path.rmdir
    empty_dir_path = Path("data/out_data/tmp/empty_dir")
    empty_dir_path.mkdir(parents=True, exist_ok=True)
    print(f"Removing empty directory {empty_dir_path} using rmdir")
    empty_dir_path.rmdir()
    print("=== Passed 3 ===")


if __name__ == "__main__":
    main()
