"""Illustrates how to read a file with a header using csv.DictReader."""

import csv
from pathlib import Path

tasks_file_path = Path("data/in_data/tasks/tasks_with_header.csv")


def main() -> None:
    """Application entry point."""
    with tasks_file_path.open() as file:
        csv_dict_reader = csv.DictReader(file)

        for rowno, row in enumerate(csv_dict_reader, start=1):
            print(f"row #{rowno}: {row}")

    print("===" * 10)

    # This can be done in one shot
    with tasks_file_path.open() as file:
        csv_dict_reader = csv.DictReader(file)
        tasks = list(csv_dict_reader)

    print(tasks)


if __name__ == "__main__":
    main()
