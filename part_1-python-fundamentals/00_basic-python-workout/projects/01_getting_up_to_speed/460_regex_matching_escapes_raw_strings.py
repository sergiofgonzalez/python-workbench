"""Illustrate how to use raw strings to match strings with escape sequences."""

import re
from pathlib import Path

base_path = Path("data", "in_data", "regex_files")


def main() -> None:
    """Application entry point."""
    file_path = base_path / "02_textfile.txt"
    # peeking into the file to see how escape sequences are represented
    with file_path.open("r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            print(f"Line {line_number}: {line.strip()} (repr: {line!r})")
    print("=" * 40)

    # matching lines with escape sequences using raw strings
    with file_path.open("r", encoding="utf-8") as file:
        # raw string to match the string "\test" literally
        pattern = re.compile(r"\\ten")
        for line_number, line in enumerate(file, start=1):
            match = pattern.search(line)
            if match:
                print(f"HIT: Line {line_number}: {line.strip()}")
    print("=" * 40)


if __name__ == "__main__":
    main()
