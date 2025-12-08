"""Illustrates how to copy files using shutil.copy2."""

import shutil
from pathlib import Path

in_dir_path = Path("data/in_data/my_files")
dst_dir_path = Path("data/out_data/tmp/copied_files")


def main() -> None:
    """Application entry point."""
    for file_path in in_dir_path.glob("*"):
        subject_id = file_path.stem
        dst_file_path = dst_dir_path / Path("subjects") / subject_id / file_path.name
        dst_file_path.parent.mkdir(parents=True, exist_ok=True)
        print(f"Copying file: {file_path} to {dst_file_path}")
        shutil.copy2(file_path, dst_file_path)


if __name__ == "__main__":
    main()
