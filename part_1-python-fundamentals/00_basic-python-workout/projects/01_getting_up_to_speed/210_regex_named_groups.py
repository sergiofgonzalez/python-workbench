"""Illustrate how to define named groups when working with regexes."""

import re
from typing import NamedTuple

db_crash_log = """101, Homework; Complete physics and math
some random nonsense
102, Laundry; Wash all the clothes today
54, random; record
103, Museum; All about Egypt
1234, random; record
Another random record"""

class TaskRecord(NamedTuple):
    """Represent a task record found in the DB crash log."""

    task_id: int
    task_name: str
    task_description: str


def main() -> None:
    """Application entry point."""
    # first, we get the lines from the log
    lines = re.split(r"\n+", db_crash_log)
    regex_pattern_valid_record = (
        r"^(?P<task_id>\d+),\s(?P<task_name>\w+);\s(?P<task_description>.+)$"
    )
    compiled_regex = re.compile(regex_pattern_valid_record)

    valid_records = []
    invalid_records = []
    for line in lines:
        match = compiled_regex.match(line)
        if match:
            task_id = match.group("task_id")
            task_name = match.group("task_name")
            task_description = match.group("task_description")
            print(f"Matched: {task_id=!r}, {task_name=!r}, {task_description=!r}")
            record = TaskRecord(
                task_id=int(task_id),
                task_name=task_name,
                task_description=task_description,
            )
            valid_records.append(record)
        else:
            print("No Match:", line.strip())
            invalid_records.append(line.strip())

    print("-" * 80)
    print("Valid Records:")
    for record in valid_records:
        print(record)
    print("-" * 80)
    print("Invalid Records:")
    for record in invalid_records:
        print(record)
    print("-" * 80)


if __name__ == "__main__":
    main()
