"""Illustrate reading file lines with readlines()."""

from pathlib import Path

tasks_file_path = Path("data/in_data/tasks/tasks.csv")


def main() -> None:
    """Application entry point."""
    with tasks_file_path.open() as file:
        lines = file.readlines()

    for rowno, line in enumerate(lines, start=1):
        print(f"row #{rowno}: {line.rstrip()}")


if __name__ == "__main__":
    main()
