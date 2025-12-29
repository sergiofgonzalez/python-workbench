"""Calculates the size of a dir tree by traversing its files and subdirectories."""

import argparse
import sys
from pathlib import Path


def get_directory_size(directory: Path, extension: str | None = None) -> int:
    """Recursively calculate the total size of files in the given directory.

    Args:
        directory (Path): The directory to calculate the size for.
        extension (str | None): If provided, only files with this extension are counted.

    Returns:
        int: Total size in bytes.
    """
    total_size = 0
    pattern = f"*{extension}" if extension else "*"
    for fp in directory.rglob(pattern):
        if fp.is_file():
            total_size += fp.stat().st_size
    return total_size


def get_human_readable_size(size_in_bytes: int) -> str:
    """Convert a size in bytes to a human-readable format.

    Args:
        size_in_bytes (int): Size in bytes.

    Returns:
        str: Human-readable size string.
    """
    size = size_in_bytes
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size < 1024:  # noqa: PLR2004
            return f"{size:.2f} {unit}"
        size /= 1024
    return f"{size:.2f} PB"


def print_results(
    *,
    total_size: int,
    directory: str,
    extension: str | None,
    human_readable: bool,
) -> None:
    """Print the results of the directory size calculation.

    Args:
        total_size (int): The total size in bytes.
        directory (str): The directory path.
        extension (str | None): The file extension filter.
        human_readable (bool): Whether to display size in a human-readable format.
    """
    report_fixed_part = (
        f"Total size of files in '{directory}'"
        f"{' with extension ' + repr(extension) if extension else ''}: "
    )
    if human_readable:
        human_readable_size = get_human_readable_size(total_size)
        print(f"{report_fixed_part}{human_readable_size}")
    else:
        print(
            f"{report_fixed_part}{total_size} {'byte' if total_size == 1 else 'bytes'}",
        )


def validate(directory: Path) -> None:
    """Validate that the provided path is a directory.

    Args:
        directory (Path): The directory path to validate.
    """
    if not directory.exists():
        print(f"The directory '{directory}' does not exist.")
        sys.exit(1)
    if not directory.is_dir():
        print(f"The path '{directory}' is not a valid directory.")
        sys.exit(1)


def main() -> None:
    """Application entry point."""
    parser = argparse.ArgumentParser(
        description="Calculate the size of a directory tree.",
    )
    parser.add_argument("directory", type=str, help="Path to the directory to analyze.")
    parser.add_argument(
        "-e",
        "--extension",
        type=str,
        help="Filter files by extension.",
        default=None,
    )
    parser.add_argument(
        "--human-readable",
        action="store_true",
        help="Display size in a human-readable format (e.g., KB, MB).",
    )
    args = parser.parse_args()

    dir_tree = Path(args.directory)
    validate(dir_tree)

    total_size = get_directory_size(dir_tree, args.extension)
    print_results(
        total_size=total_size,
        directory=args.directory,
        extension=args.extension,
        human_readable=args.human_readable,
    )


if __name__ == "__main__":
    main()
