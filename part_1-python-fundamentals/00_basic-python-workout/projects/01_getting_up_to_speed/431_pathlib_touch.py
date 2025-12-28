"""Illustrates how to use pathlib.Path.touch()."""

from datetime import UTC, datetime
from pathlib import Path

tmp = Path("data") / "out_data" / "tmp"


def main() -> None:
    """Application entry point."""
    new_file = tmp / "new_file.txt"
    new_file.touch(exist_ok=True)
    print(f"Created file: {new_file}")
    print("=" * 40)

    existing_file = tmp / ".gitkeep"
    stat_before = existing_file.stat()
    # Print the timestamps in human-readable format before touching
    print(
        f"Before touch: {existing_file} - created at  "
        f"{datetime.fromtimestamp(stat_before.st_ctime, tz=UTC)}",
    )
    print(
        f"Before touch: {existing_file} - modified at "
        f"{datetime.fromtimestamp(stat_before.st_mtime, tz=UTC)}",
    )
    print(
        f"Before touch: {existing_file} - accessed at "
        f"{datetime.fromtimestamp(stat_before.st_atime, tz=UTC)}",
    )
    existing_file.touch()
    stat_after = existing_file.stat()
    # Print the timestamps in human-readable format after touching
    print(
        f"After touch : {existing_file} - created at  "
        f"{datetime.fromtimestamp(stat_after.st_ctime, tz=UTC)}",
    )
    print(
        f"After touch : {existing_file} - modified at "
        f"{datetime.fromtimestamp(stat_after.st_mtime, tz=UTC)}",
    )
    print(
        f"After touch : {existing_file} - accessed at "
        f"{datetime.fromtimestamp(stat_after.st_atime, tz=UTC)}",
    )


if __name__ == "__main__":
    main()
