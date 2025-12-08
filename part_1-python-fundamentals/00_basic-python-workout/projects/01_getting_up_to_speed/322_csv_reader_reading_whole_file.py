"""Illustrate how to read a whole CSV file at once."""

import csv
from pathlib import Path

tasks_file_path = Path("data/in_data/tasks/tasks.csv")


def main() -> None:
    """Application entry point."""
    with tasks_file_path.open() as file:
        csv_reader = csv.reader(file)
        rows = list(csv_reader)

    print(rows)


if __name__ == "__main__":
    main()
