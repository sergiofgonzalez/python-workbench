"""__init__.py file for the utils package."""

from shortcut_prefix_renamer.utils.fileutils import find_files_with_prefix, rename_files
from shortcut_prefix_renamer.utils.reporting import (
    report_files_with_prefix_found,
    report_rename_completion,
)
from shortcut_prefix_renamer.utils.validator import fail_if_not_valid_root_dir

__all__ = [
    "fail_if_not_valid_root_dir",
    "find_files_with_prefix",
    "rename_files",
    "report_files_with_prefix_found",
    "report_rename_completion",
]
