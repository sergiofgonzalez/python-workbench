"""Filtering files in a directory using pathlib.glob."""

from pathlib import Path

dir_path = Path("data/in_data/my_files")


def main() -> None:
    """Application entry point."""
    pattern = "*.dat"
    print(f"Searching for files in {dir_path} matching pattern '{pattern}':")
    for file_path in dir_path.glob(pattern):
        print(f"Found file: {file_path}")
    print("=" * 40)

    # testing different patterns: you need to include the * at the start
    pattern = ".dat"
    print(f"Searching for files in {dir_path} matching pattern '{pattern}':")
    for file_path in dir_path.glob(pattern):
        print(f"Found file: {file_path}")


if __name__ == "__main__":
    main()
