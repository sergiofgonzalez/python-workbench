"""Basic program that copies and renames files matching a wildcard pattern."""

import shutil
from pathlib import Path


def main() -> None:
    """Application entry point."""
    src_dir = Path("data/in_data/132_copying_and_renaming_files")
    dest_dir = Path("data/out_data/132_copying_and_renaming_files")
    dest_dir.mkdir(parents=True, exist_ok=True)
    prefix_pattern = "photo"
    wildcard_pattern = "IMG_*.jpg"

    # Copy files matching the wildcard pattern
    for i, file_path in enumerate(src_dir.glob(wildcard_pattern)):
        out_file_path = dest_dir / f"{prefix_pattern}_{i + 1}{file_path.suffix}"
        shutil.copy2(file_path, out_file_path)
        print(f"{file_path} => {out_file_path}")



if __name__ == "__main__":
    main()
