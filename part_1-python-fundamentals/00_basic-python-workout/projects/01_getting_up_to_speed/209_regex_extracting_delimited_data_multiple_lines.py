"""Illustrate how to extract delimited data from multiple lines using regex."""

import re
from typing import NamedTuple


class TaskRecord(NamedTuple):
    """Represent a task record found in the DB crash log."""

    task_id: int
    task_name: str
    task_description: str


def main() -> None:  # noqa: C901, PLR0912, PLR0915
    """Application entry point."""
    # Simulate a DB crash log with some valid and invalid records
    db_crash_log = """101, Homework; Complete physics and math
some random nonsense
102, Laundry; Wash all the clothes today
54, random; record
103, Museum; All about Egypt
1234, random; record
Another random record"""

    print(db_crash_log)
    print("-" * 80)

    # findall() will help us to extract all the valid records
    regex_pattern_valid_record = r"(\d+),\s(\w+); (.+)"
    matches = re.findall(regex_pattern_valid_record, db_crash_log)
    for match in matches:
        print(match)
    print("-" * 80)

    # but we need to get a report of valid and invalid records
    # so we will use re.finditer() which returns an iterator yielding
    # match objects over all non-overlapping matches for the RE pattern
    # in the string. This will allow us to get the start and end positions
    # of each match and compare it with the previous match end position
    # This however doesn't work 100% as we don't get the last invalid record
    # and we get additional invalid records with newline characters
    matches = re.finditer(regex_pattern_valid_record, db_crash_log)
    last_end = 0
    for match in matches:
        start, end = match.span()
        if start != last_end:
            print("No Match:", db_crash_log[last_end:start].strip())
        task_id, task_name, task_description = match.groups()
        print(f"Matched: {task_id=!r}, {task_name=!r}, {task_description=!r}")
        last_end = end
    print("-" * 80)

    # another try using re.split() using a divide and conquer approach
    # splitting the text into lines and processing each line separately
    # This one works perfectly
    lines = re.split(r"\n+", db_crash_log)
    for line in lines:
        match = re.match(regex_pattern_valid_record, line)
        if match:
            task_id, task_name, task_description = match.groups()
            print(f"Matched: {task_id=!r}, {task_name=!r}, {task_description=!r}")
        else:
            print("No Match:", line.strip())
    print("-" * 80)

    # Now we can wrap it all up by creating NamedTuples for the valid records
    # and a list of strings for the invalid records
    valid_records = []
    invalid_records = []
    for line in lines:
        match = re.match(regex_pattern_valid_record, line)
        if match:
            task_id, task_name, task_description = match.groups()
            record = TaskRecord(int(task_id), task_name, task_description)
            valid_records.append(record)
        else:
            invalid_records.append(line.strip())

    print("Valid Records:")
    for record in valid_records:
        print(f" - {record}")
    print("Invalid Records:")
    for record in invalid_records:
        print(f" - {record}")
    print("-" * 80)

    # I've noticed that the regex pattern could be improved by adding boundary
    # anchors to ensure that we match the whole line
    regex_pattern_valid_record = r"^(\d+),\s(\w+);\s(.+)$"
    valid_records = []
    invalid_records = []
    for line in lines:
        match = re.match(regex_pattern_valid_record, line)
        if match:
            task_id, task_name, task_description = match.groups()
            record = TaskRecord(int(task_id), task_name, task_description)
            valid_records.append(record)
        else:
            invalid_records.append(line.strip())

    print("Valid Records:")
    for record in valid_records:
        print(f" - {record}")
    print("Invalid Records:")
    for record in invalid_records:
        print(f" - {record}")
    print("-" * 80)

    # Also, as we use the regex pattern multiple times, we can compile it
    # and use the indexed groups for clarity
    regex_compiled = re.compile(regex_pattern_valid_record)
    valid_records = []
    invalid_records = []
    for line in lines:
        match = regex_compiled.match(line)
        if match:
            task_id = match.group(1)
            task_name = match.group(2)
            task_description = match.group(3)
            record = TaskRecord(int(task_id), task_name, task_description)
            valid_records.append(record)
        else:
            invalid_records.append(line.strip())
    print("Valid Records:")
    for record in valid_records:
        print(f" - {record}")
    print("Invalid Records:")
    for record in invalid_records:
        print(f" - {record}")
    print("-" * 80)


if __name__ == "__main__":
    main()
