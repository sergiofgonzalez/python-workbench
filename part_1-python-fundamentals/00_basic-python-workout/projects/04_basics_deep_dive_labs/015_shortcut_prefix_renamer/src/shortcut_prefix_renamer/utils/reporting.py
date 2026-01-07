"""Reporting utilities for purge-venv."""

import os
from pathlib import Path


def get_root_dir_name(root_dir: Path) -> str:
    """Get the name of the directory if the root directory is '.' or '..'.

    Args:
        root_dir (Path): The root directory path.

    Returns:
        str: The name of the root directory.
    """
    if root_dir in (Path(os.curdir), Path(os.pardir)):
        return f"{root_dir.resolve().name}{os.sep}"
    if not str(root_dir).endswith(os.sep):
        return f"{root_dir}{os.sep}"
    return str(root_dir)


def report_files_with_prefix_found(
    root_dir: Path,
    files_with_prefix: list[Path],
    prefix: str,
) -> None:
    """Report files found with the given prefix.

    Args:
        root_dir (str): The root directory searched.
        files_with_prefix (list[str]): List of found files with the given prefix.
        prefix (str): The prefix searched for.
    """
    if not files_with_prefix:
        print(
            f"No files found with prefix '{prefix}' within "
            f"{get_root_dir_name(root_dir)}.",
        )
        return

    report_lines = []
    report_lines.extend(
        [
            f"Found {len(files_with_prefix)} file"
            f"{'s' if len(files_with_prefix) != 1 else ''} starting with prefix "
            f"'{prefix}' within {get_root_dir_name(root_dir)}:",
        ],
    )

    for file_with_prefix in files_with_prefix:
        report_lines.append(  # noqa: PERF401
            f"- {file_with_prefix.relative_to(root_dir)}",
        )
    print("\n".join(report_lines))


def report_rename_completion(status_messages: list[str]) -> None:
    """Report the completion of the rename process.

    Args:
        status_messages (list[str]): List of status messages from renaming.
    """
    for msg in status_messages:
        print(msg)
