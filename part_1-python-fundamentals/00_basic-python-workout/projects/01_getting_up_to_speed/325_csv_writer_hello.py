"""Illustrates how to write a CSV using csv.writer()."""

import csv
from pathlib import Path

out_tasks_file_path = Path("data/out_data/tmp/tasks.csv")


def print_file_contents(path: Path) -> None:
    """Print the contents of the file given."""
    with path.open() as file:
        data = file.read()
        print(f"{data!r}")


def main() -> None:
    """Application entry point."""
    rows_for_csv = [
        ["task_id", "title", "urgency"],
        ["1001", "Homework", 5],
        ["1002", "Laundry", 3],
        ["1003", "Grocery", 4],
    ]

    with out_tasks_file_path.open("w", newline="") as file:
        csv_writer = csv.writer(file)
        for row in rows_for_csv:
            csv_writer.writerow(row)

    # Now we validate what's been written
    print_file_contents(out_tasks_file_path)
    print("=" * 40)

    # We could have written the file with writerows, as we knew what we had
    # to write upfront
    with out_tasks_file_path.open("w", newline="") as file:
        csv_writer = csv.writer(file)
        csv_writer.writerows(rows_for_csv)

    # Validate what's been written with writerows
    print_file_contents(out_tasks_file_path)
    print("=" * 40)

    # Now we add a new line
    with out_tasks_file_path.open("a", newline="") as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(["1004", "Museum", 3])

    # Validate what's been written after appending
    print_file_contents(out_tasks_file_path)
    print("=" * 40)

if __name__ == "__main__":
    main()
