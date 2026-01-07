"""Module for finding virtual environment directories."""

from collections.abc import Generator
from pathlib import Path


def find_files_with_prefix(root_dir: Path, prefix: str) -> list[Path]:
    """Recursively find files with given prefix in and below the given root directory.

    Args:
        root_dir (Path): The root directory to search.
        prefix (str): The prefix to look for in filenames.

    Returns:
        list[Path]: List of paths to found files with the given prefix.
    """
    found_dirs = []
    root_path = Path(root_dir)

    for file_path in root_path.rglob(f"{prefix}*"):
        if file_path.is_file():
            found_dirs.append(file_path)  # noqa: PERF401

    return sorted(found_dirs)


def generate_candidate_paths(base_path: Path) -> Generator[Path, None, None]:
    """Generate candidate paths: original name, then with _001, _002, etc."""
    yield base_path
    for i in range(1, 1000):
        suffixed_name = f"{base_path.stem}_{i:03d}{base_path.suffix}"
        yield base_path.with_name(suffixed_name)


def rename_file(file_path: Path, prefix: str, *, dry_run: bool = False) -> str:
    """Rename a single file by removing the given prefix.

    Args:
        file_path (Path): The path to the file to rename.
        prefix (str): The prefix to remove from the filename.
        dry_run (bool): If True, do not actually rename the file.

    Returns:
        str: Message informing about the renaming process of the file.
    """
    new_name = file_path.name[len(prefix) :]
    new_path = file_path.with_name(new_name)

    for candidate_path in generate_candidate_paths(new_path):
        if candidate_path.exists():
            continue
        if not dry_run:
            file_path.rename(candidate_path)
        return f"Renamed: {file_path} -> {candidate_path}"

    return (
        f"Failed to rename {file_path}: could not find a unique name after "
        f"999 attempts."
    )


def rename_files(files: list[Path], prefix: str, *, dry_run: bool = False) -> list[str]:
    """Rename the given files.

    Args:
        files (list[Path]): List of files to rename.
        prefix (str): The prefix to remove from filenames.
        dry_run (bool): If True, do not actually rename the files.

    Returns:
        list[str]: List of messages informing about the renaming process of each file.
    """
    status_messages = []
    for file_path in files:
        try:
            # Remove the prefix from the filename
            status_message = rename_file(file_path, prefix, dry_run=dry_run)
            status_messages.append(status_message)
        except Exception as e:  # noqa: BLE001
            status_messages.append(f"Error renaming {file_path}: {e}")
            print(f"Error renaming {file_path}: {e}")
    return status_messages
