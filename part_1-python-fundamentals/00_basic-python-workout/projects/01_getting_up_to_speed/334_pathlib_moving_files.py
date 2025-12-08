"""Illustrates moving files using pathlib."""

import shutil
from pathlib import Path

in_dir_path = Path("data/in_data/my_files")
dst_dir_path = Path("data/out_data/tmp/moved_files")


def main() -> None:
    """Application entry point."""
    # We first make a mirror of the input directory to move files from
    mirror_dir_path = Path("data/out_data/tmp/mirror_files")
    shutil.copytree(in_dir_path, mirror_dir_path, dirs_exist_ok=True)

    # Now we move files from the mirror directory to the destination directory

    for file_path in mirror_dir_path.glob("*"):
        subject_id = file_path.stem
        dst_file_path = dst_dir_path / Path("subjects") / subject_id / file_path.name
        dst_file_path.parent.mkdir(parents=True, exist_ok=True)
        print(f"Moving file: {file_path} to {dst_file_path}")
        file_path.rename(dst_file_path)


if __name__ == "__main__":
    main()
