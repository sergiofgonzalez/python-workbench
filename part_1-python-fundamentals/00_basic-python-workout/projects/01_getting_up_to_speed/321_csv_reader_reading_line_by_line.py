"""Reading a CSV file with a `csv.reader`."""

import csv
from pathlib import Path

tasks_file_path = Path("data/in_data/tasks/tasks.csv")


def main() -> None:
    """Application entry point."""
    with tasks_file_path.open() as file:
        csv_reader = csv.reader(file)

        for rowno, row in enumerate(csv_reader, start=1):
            print(f"row #{rowno}: {row}")


if __name__ == "__main__":
    main()
