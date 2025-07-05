"""Illustrate how to use / to build paths."""

from pathlib import Path


def main() -> None:
    """Application entry point."""
    # Create a Path object for the current directory
    current_dir = Path(".")

    # Build a path to a file named 'example.txt' in the current directory
    file_path = current_dir / "example.txt"
    print(f"Path to file: {file_path}")

    # Build a path to a subdirectory named 'subdir' and a file 'data.txt' within it
    subdir_file_path = current_dir / "subdir" / "data.txt"
    print(f"Path to subdirectory file: {subdir_file_path}")

    # Build a path to a parent directory and a file 'config.yaml'
    parent_file_path = current_dir.parent / "config.yaml"
    print(f"Path to parent directory file: {parent_file_path}")


if __name__ == "__main__":
    main()
