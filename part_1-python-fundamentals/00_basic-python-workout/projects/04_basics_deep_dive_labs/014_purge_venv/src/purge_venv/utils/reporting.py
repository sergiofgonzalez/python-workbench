"""Reporting utilities for purge-venv."""

import os
from pathlib import Path

from purge_venv.utils.dirutils import get_directory_size


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


def report_venvs_found(
    root_dir: Path,
    venv_dirs: list[Path],
    venv_names: list[str],
) -> None:
    """Report found virtual environment directories.

    Args:
        root_dir (str): The root directory searched.
        venv_dirs (list[str]): List of found virtual environment directory paths.
        venv_names (list[str]): List of virtual environment directory names
            searched for.
    """
    if not venv_dirs:
        print(
            f"No virtual environment directories found within {root_dir} "
            f"({', '.join(venv_names)}).",
        )
        return

    report_lines = []
    total_size_bytes = 0
    report_lines.extend(
        [
            f"Found {len(venv_dirs)} virtual environment "
            f"director{'y' if len(venv_dirs) == 1 else 'ies'} "
            f"within {get_root_dir_name(root_dir)} ({', '.join(venv_names)}):",
        ],
    )

    for venv_dir in venv_dirs:
        dir_size_bytes = get_directory_size(venv_dir)
        total_size_bytes += dir_size_bytes
        report_lines.append(
            f"- {venv_dir.relative_to(root_dir)}: "
            f"{get_human_readable_size(dir_size_bytes)}",
        )
    report_lines.append(
        f"(Total size: {get_human_readable_size(total_size_bytes)})",
    )
    print("\n".join(report_lines))


def report_dir_size_before_after_purge(root_dir: Path, *, before: bool) -> None:
    """Report the size of the root directory before or after purge.

    Args:
        root_dir (Path): The root directory path.
        before (bool): If True, report size before purge; else after purge.
    """
    total_size_bytes = get_directory_size(root_dir)
    print(
        f"Total size of '{get_root_dir_name(root_dir)}' "
        f"{'before' if before else 'after'} purge: "
        f"{get_human_readable_size(total_size_bytes)}",
    )


def report_purge_completion(err_messages: list[str]) -> None:
    """Report the completion of the purge process.

    Args:
        err_messages (list[str]): List of error messages encountered during deletion.
    """
    if err_messages:
        print("Purge completed with errors:")
        print("Some errors occurred during deletion:")
        for msg in err_messages:
            print(f"- {msg}")
    else:
        print("Purge completed successfully without errors.")
