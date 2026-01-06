"""purge-venv: purge virtual environments directories from a given directory."""

import argparse
import signal
import sys
from pathlib import Path

from purge_venv.utils import (
    delete_dirs,
    fail_if_not_valid_root_dir,
    fail_if_too_many_venv_names,
    find_venv_dirs,
    report_dir_size_before_after_purge,
    report_purge_completion,
    report_venvs_found,
)


def handle_sigint(signum: int, frame: object) -> None:  # noqa: ARG001
    """Handle SIGINT (Ctrl+C) gracefully."""
    print("\n\nOperation cancelled by user.")
    sys.exit(0)


signal.signal(signal.SIGINT, handle_sigint)


def main() -> None:
    """Application entry point."""
    parser = argparse.ArgumentParser(
        description="Purge virtual environment directories from a given directory.",
    )
    parser.add_argument(
        "directory",
        type=str,
        help="The root directory to search for virtual environments.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show which directories would be deleted without actually deleting them.",
    )
    parser.add_argument(
        "--venv-names",
        type=str,
        nargs="*",
        default=[".venv"],
        help="Names of virtual environment directories to look for.",
    )

    args = parser.parse_args()

    root_dir = Path(args.directory)
    report_dir_size_before_after_purge(root_dir, before=True)
    if args.dry_run:
        print("Dry run mode enabled. No directories will be deleted.")

    fail_if_too_many_venv_names(
        [],
        max_allowed=5,
    )
    fail_if_not_valid_root_dir(root_dir)

    venv_dirs_found = find_venv_dirs(root_dir, args.venv_names)
    report_venvs_found(root_dir, venv_dirs_found, args.venv_names)
    if not venv_dirs_found:
        return
    print("This action would delete the above virtual environment directories.")
    confirmation = input("Are you sure you want to proceed? (y/N): ").strip().lower()
    if confirmation == "y":
        if not args.dry_run:
            err_messages = delete_dirs(venv_dirs_found)
            report_purge_completion(err_messages)
            report_dir_size_before_after_purge(root_dir, before=False)
        else:
            print("Dry run complete. No directories were deleted.")
    else:
        print("Purge cancelled by user.")
        return


if __name__ == "__main__":
    main()
