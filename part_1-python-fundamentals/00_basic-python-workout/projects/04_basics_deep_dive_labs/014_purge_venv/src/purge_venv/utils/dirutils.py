"""Module for finding virtual environment directories."""

import shutil
from pathlib import Path


def find_venv_dirs(root_dir: Path, venv_names: list[str]) -> list[Path]:
    """Recursively find virtual environment dirs in and below the given root directory.

    Args:
        root_dir (Path): The root directory to search.
        venv_names (list[str]): List of virtual environment directory names to look for.

    Returns:
        list[Path]: List of paths to found virtual environment directories.
    """
    found_dirs = []
    root_path = Path(root_dir)

    for venv_name in venv_names:
        for venv_path in root_path.rglob(venv_name):
            if venv_path.is_dir():
                found_dirs.append(venv_path)  # noqa: PERF401

    return sorted(found_dirs)


def get_directory_size(directory: Path) -> int:
    """Recursively calculate the total size of files in the given directory.

    Args:
        directory (Path): The directory to calculate the size for.

    Returns:
        int: Total size in bytes.
    """
    total_size = 0
    for fp in directory.rglob("*"):
        if fp.is_file():
            total_size += fp.stat().st_size
    return total_size


def delete_dirs(directories: list[Path]) -> list[str]:
    """Delete the given directories.

    Args:
        directories (list[Path]): List of directories to delete.

    Returns:
        list[str]: List of error messages encountered during deletion.
    """
    err_messages = []
    for venv_dir in directories:
        try:
            shutil.rmtree(venv_dir)
        except Exception as e:  # noqa: BLE001
            err_messages.append(f"Error deleting {venv_dir}: {e}")
            print(f"Error deleting {venv_dir}: {e}")
    return err_messages
