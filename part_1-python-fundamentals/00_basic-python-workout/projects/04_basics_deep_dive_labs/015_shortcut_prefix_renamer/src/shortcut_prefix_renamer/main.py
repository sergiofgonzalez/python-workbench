"""Shortcut prefix renamer."""

import argparse
import signal
import sys
from pathlib import Path

from shortcut_prefix_renamer.utils import (
    fail_if_not_valid_root_dir,
    find_files_with_prefix,
    rename_files,
    report_files_with_prefix_found,
    report_rename_completion,
)


def handle_sigint(signum: int, frame: object) -> None:  # noqa: ARG001
    """Handle SIGINT (Ctrl+C) gracefully."""
    print("\n\nOperation cancelled by user.")
    sys.exit(0)


signal.signal(signal.SIGINT, handle_sigint)


def main() -> None:
    """Application entry point."""
    parser = argparse.ArgumentParser(
        description=(
            "Renames the shortcut prefixes in filenames such as "
            "'Link to ' or 'Shortcut to '."
        ),
    )
    parser.add_argument(
        "directory",
        type=str,
        help="The root directory to search for files with shortcut prefixes.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show which files would be renamed without actually renaming them.",
    )
    parser.add_argument(
        "--shortcut-prefix",
        type=str,
        default="Link to",
        help="The shortcut prefix to look for in filenames.",
    )

    args = parser.parse_args()

    root_dir = Path(args.directory)
    prefix = args.shortcut_prefix + " "
    if args.dry_run:
        print("Dry run mode enabled. No files will be renamed.")

    fail_if_not_valid_root_dir(root_dir)

    files_with_prefix_found = find_files_with_prefix(
        root_dir,
        prefix,
    )
    report_files_with_prefix_found(
        root_dir,
        files_with_prefix_found,
        prefix,
    )
    if not files_with_prefix_found:
        print("No files to rename. Exiting.")
        return

    print("This action would rename the files listed above removing their prefix.")
    confirmation = input("Are you sure you want to proceed? (y/N): ").strip().lower()
    if confirmation == "y":
        status_messages = rename_files(
            files_with_prefix_found,
            prefix,
            dry_run=args.dry_run,
        )
        report_rename_completion(status_messages)
        if args.dry_run:
            print("Dry run complete. No files were renamed.")
    else:
        print("Purge cancelled by user.")
        return


if __name__ == "__main__":
    main()
