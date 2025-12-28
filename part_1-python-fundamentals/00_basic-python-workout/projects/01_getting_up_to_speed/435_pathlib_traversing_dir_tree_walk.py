"""Illustrate how to traverse directory trees using pathlib.Path.walk()."""

from pathlib import Path


def main() -> None:
    """Application entry point."""
    cur_dir = Path()  # Current directory
    for root, dirs, files in cur_dir.walk():
        print(f"Root: {root}")
        print(f"Directories: {dirs}")
        print(f"Files: {files}")
        if ".venv" in dirs:
            print("=> .venv directory will be ignored.")
            dirs.remove(".venv")  # Skip virtual environment directories
        if "__pycache__" in dirs:
            print("=> __pycache__ directory will be ignored.")
            dirs.remove("__pycache__")  # Skip __pycache__ directories
        print("-" * 40)


if __name__ == "__main__":
    main()
