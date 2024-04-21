"""Entry point for the application."""

import csv
import sys


def read_csv(filename: str) -> list[list[str]]:
    """Read a CSV file and return a list of tuples."""
    with open(filename, encoding="utf-8") as file:
        info = [row for row in csv.reader(file, delimiter="|")]
        return info


if __name__ == "__main__":
    data = read_csv(sys.argv[1])
    # Print the first 5 rows of the CSV file
    for row in data[0:5]:
        print(row)
