"""Illustrates how to write a CSV using csv.DictWriter()."""

import csv
from pathlib import Path

tasks_file_path = Path("data/out_data/tmp/tasks.csv")


tasks = [
    {"task_id": "1001", "title": "Homework", "urgency": "5"},
    {"task_id": "1002", "title": "Laundry", "urgency": "3"},
    {"task_id": "1003", "title": "Grocery", "urgency": "4"},
]

def print_file_contents(path: Path) -> None:
    """Print the contents of the file given."""
    with path.open() as file:
        data = file.read()
        print(f"{data!r}")


def main() -> None:
    """Application entry point."""
    with tasks_file_path.open("w", newline="") as file:
        dict_writer = csv.DictWriter(file, fieldnames=["task_id", "title", "urgency"])
        dict_writer.writeheader()
        dict_writer.writerows(tasks)

    # Validate what's been written
    print_file_contents(tasks_file_path)
    print("=" * 40)

    # We could have extracted the keys from the one of the dicts to write
    with tasks_file_path.open("w", newline="") as file:
        dict_writer = csv.DictWriter(file, fieldnames=tasks[0].keys())
        dict_writer.writeheader()
        dict_writer.writerows(tasks)

    # Validate what's been written
    print_file_contents(tasks_file_path)
    print("=" * 40)

    # Obviously, we could have written the rows one by one
    with tasks_file_path.open("w", newline="") as file:
        dict_writer = csv.DictWriter(file, fieldnames=tasks[0].keys())
        dict_writer.writeheader()
        for task in tasks:
            dict_writer.writerow(task)

    # Validate what's been written
    print_file_contents(tasks_file_path)
    print("=" * 40)

if __name__ == "__main__":
    main()
