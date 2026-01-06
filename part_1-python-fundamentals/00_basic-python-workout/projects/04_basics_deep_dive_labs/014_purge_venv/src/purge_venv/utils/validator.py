"""Validation utilities for purge-venv."""

import sys
from pathlib import Path


def fail_if_not_valid_root_dir(directory: Path) -> None:
    """Check if the provided name is a valid virtual environment directory name.

    Args:
        directory (Path): The directory to validate.

    Raises:
        SystemExit: If the directory does not exist or is not a directory.
    """
    if not directory.exists():
        sys.exit(f"Error: The directory '{directory}' does not exist.")
    if not directory.is_dir():
        sys.exit(f"Error: The path '{directory}' is not a directory.")


def fail_if_too_many_venv_names(venv_names: list[str], max_allowed: int = 5) -> None:
    """Check if the number of venv names to seek for exceeds the allowed max.

    Args:
        venv_names (list[str]): List of virtual environment directory names to look for.
        max_allowed (int): Maximum allowed number of virtual environment dir names.

    Raises:
        SystemExit: If the number of found directories exceeds the maximum allowed.
    """
    if len(venv_names) > max_allowed:
        sys.exit(
            f"Error: Too many virtual environment directory names provided "
            f"({len(venv_names)}). Maximum allowed is {max_allowed}.",
        )
