"""Illustrates counting lines matching a regex pattern in a file."""

import re
from pathlib import Path

base_path = Path("data", "in_data", "regex_files")


def main() -> None:  # noqa: C901, PLR0915
    """Application entry point."""
    file_path = base_path / "01_textfile.txt"

    # using the OOP approach
    with file_path.open("r", encoding="utf-8") as file:
        pattern = re.compile(r"\bhello\b")
        hits = 0
        for line_number, line in enumerate(file, start=1):
            match = pattern.search(line)
            if match:
                print(f"Line {line_number}: {line.strip()}")
                hits += 1
        print(f"Total lines matching pattern: {hits}")
    print("=" * 40)

    # using the functional approach
    with file_path.open("r", encoding="utf-8") as file:
        hits = 0
        for line_number, line in enumerate(file, start=1):
            match = re.search(r"\bhello\b", line)
            if match:
                print(f"Line {line_number}: {line.strip()}")
                hits += 1
        print(f"Total lines matching pattern: {hits}")
    print("=" * 40)

    # enhancement: case insensitive matching: option 1
    with file_path.open("r", encoding="utf-8") as file:
        pattern = re.compile(r"\b(?P<first_match>[Hh]ello)\b")
        hits = 0
        for line_number, line in enumerate(file, start=1):
            match = pattern.search(line)
            if match:
                print(
                    f"Line {line_number}: {line.strip()} "
                    f"(found: {match.group('first_match')!r} "
                    f"in position {match.start()}-{match.end()})",
                )
                hits += 1
        print(f"Total lines matching pattern: {hits}")
    print("=" * 40)

    # enhancement: case insensitive matching: option 2
    with file_path.open("r", encoding="utf-8") as file:
        pattern = re.compile(r"\b(?P<first_match>(H|h)ello)\b")
        hits = 0
        for line_number, line in enumerate(file, start=1):
            match = pattern.search(line)
            if match:
                print(
                    f"Line {line_number}: {line.strip()} "
                    f"(found: {match.group('first_match')!r} "
                    f"in position {match.start()}-{match.end()})",
                )
                hits += 1
        print(f"Total lines matching pattern: {hits}")
    print("=" * 40)

    # enhancement: case insensitive matching: option 3
    with file_path.open("r", encoding="utf-8") as file:
        pattern = re.compile(r"\b(?P<first_match>Hello|hello)\b")
        hits = 0
        for line_number, line in enumerate(file, start=1):
            match = pattern.search(line)
            if match:
                print(
                    f"Line {line_number}: {line.strip()} "
                    f"(found: {match.group('first_match')!r} "
                    f"in position {match.start()}-{match.end()})",
                )
                hits += 1
        print(f"Total lines matching pattern: {hits}")
    print("=" * 40)

    # enhancement: case insensitive matching: option 4
    with file_path.open("r", encoding="utf-8") as file:
        pattern = re.compile(r"\b(?P<first_match>hello)\b", re.IGNORECASE)
        hits = 0
        for line_number, line in enumerate(file, start=1):
            match = pattern.search(line)
            if match:
                print(
                    f"Line {line_number}: {line.strip()} "
                    f"(found: {match.group('first_match')!r} "
                    f"in position {match.start()}-{match.end()})",
                )
                hits += 1
        print(f"Total lines matching pattern: {hits}")
    print("=" * 40)


if __name__ == "__main__":
    main()
