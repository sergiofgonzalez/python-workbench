"""Illustrate how to use groupdict with named groups in regex."""

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

    valid_dicts = []
    valid_records = []
    invalid_records = []
    for line in lines:
        match = compiled_regex.match(line)
        if match:
            # use groupdict() to get a dictionary of named groups
            # as in {'task_id': '...', 'task_name': '...', 'task_description': '...'}
            group_dict = match.groupdict()
            print(f"Matched: {group_dict}")
            valid_dicts.append(group_dict)
            record = TaskRecord(
                task_id=int(group_dict["task_id"]),
                task_name=group_dict["task_name"],
                task_description=group_dict["task_description"],
            )
            valid_records.append(record)
        else:
            print("No Match:", line.strip())
            invalid_records.append(line.strip())
    print("-" * 80)
    print("Valid Dicts:")
    print(valid_dicts)

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
