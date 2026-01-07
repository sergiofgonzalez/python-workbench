"""Validation utilities for purge-venv."""

import sys
from pathlib import Path


def fail_if_not_valid_root_dir(directory: Path) -> None:
    """Check if the provided name is a valid root directory.

    Args:
        directory (Path): The directory to validate.

    Raises:
        SystemExit: If the directory does not exist or is not a directory.
    """
    if not directory.exists():
        sys.exit(f"Error: The directory '{directory}' does not exist.")
    if not directory.is_dir():
        sys.exit(f"Error: The path '{directory}' is not a directory.")
