"""Illustrates how to retrieve file metadata using pathlib.Path.stat()."""

import time
from pathlib import Path

in_dir_path = Path("data/in_data/my_files")


def main() -> None:
    """Application entry point."""
    for dat_file in in_dir_path.glob("*.dat"):
        data_file_stats = dat_file.stat()
        print(f"{dat_file.name}: {data_file_stats}")
        # Printing human-readable timestamps
        print(f"  Created: {time.ctime(data_file_stats.st_ctime)}")
        print(f"  Modified: {time.ctime(data_file_stats.st_mtime)}")
        print(f"  Accessed: {time.ctime(data_file_stats.st_atime)}")
        print("=" * 40)


if __name__ == "__main__":
    main()
