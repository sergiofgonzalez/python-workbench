"""Illustrates how to delete files using pathlib.unlink."""

import shutil
from pathlib import Path

in_dir_path = Path("data/in_data/my_files")
dst_dir_path = Path("data/out_data/tmp/moved_files")


def main() -> None:
    """Application entry point."""
    # We first make a mirror of the input directory to move files from
    mirror_dir_path = Path("data/out_data/tmp/mirror_files")
    shutil.copytree(in_dir_path, mirror_dir_path, dirs_exist_ok=True)

    # Now we delete files from the mirror directory
    for file_path in mirror_dir_path.glob("*.txt"):
        print(f"Deleting file: {file_path}")
        file_path.unlink()


if __name__ == "__main__":
    main()
