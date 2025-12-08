"""Illustrates reading a CSV file with a header manually."""

import csv
from pathlib import Path

tasks_file_path = Path("data/in_data/tasks/tasks_with_header.csv")


def main() -> None:
    """Application entry point."""
    tasks = []
    with tasks_file_path.open() as file:
        csv_reader = csv.reader(file)
        header = next(csv_reader)  # Read the header row
        print(f"Header: {header}")

        for rowno, row in enumerate(csv_reader, start=1):
            print(f"row #{rowno}: {row}")
            task = dict(zip(header, row, strict=True))
            tasks.append(task)

    print(tasks)
    print("===" * 10)

    # This can also be done with a dict comprehension
    with tasks_file_path.open() as file:
        csv_reader = csv.reader(file)
        header = next(csv_reader)  # Read the header row
        print(f"Header: {header}")
        tasks = [
            dict(zip(header, row, strict=True))
            for row in csv_reader
        ]

    print(tasks)

if __name__ == "__main__":
    main()
