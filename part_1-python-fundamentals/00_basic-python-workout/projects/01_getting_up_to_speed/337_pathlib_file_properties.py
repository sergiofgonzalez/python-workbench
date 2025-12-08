"""Illustrate pathlib.Path file properties."""

import shutil
from pathlib import Path

in_dir_path = Path("data/in_data/my_files")
dst_dir_path = Path("data/out_data/tmp/moved_files")


def setup_subject_dirs() -> None:
    """Change the original structure into a different one with a dir for subject."""
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
    print("=== subject dirs done ===")


def main() -> None:
    """Application entry point."""
    setup_subject_dirs()

    # Now we do the exercise, locating the *.dat files
    for dat_file in dst_dir_path.glob("**/*.dat"):
        print(f"{dat_file=}")
        print(f"{dat_file.name=}")
        print(f"{dat_file.stem=}")
        print(f"{dat_file.suffix=}")
        print(f"{dat_file.parent=}")
        print(f"{list(dat_file.parents)=}")
        print("=" * 40)


if __name__ == "__main__":
    main()
