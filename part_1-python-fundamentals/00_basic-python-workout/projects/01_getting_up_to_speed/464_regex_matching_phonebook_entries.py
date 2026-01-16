"""Illustrates regex matching for parsing phonebook entries."""

import re
from pathlib import Path

base_path = Path("data", "in_data", "regex_files")


def default_country_code(match: re.Match) -> str:
    """Return the default country code."""
    return match.group("country_code") if match.group("country_code") else "1"


def main() -> None:
    """Application entry point."""
    file_path = base_path / "05_textfile.txt"

    # peeking into the file to see how escape sequences are represented
    with file_path.open("r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            print(f"Line {line_number}: {line.strip()} (repr: {line!r})")
    print("=" * 40)

    # parsing file entries now
    with file_path.open("r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            pattern = re.compile(
                r"^(?P<surname>\w+),\s"
                r"(?P<first_name>\w+)"
                r"(\s(?P<middle_name>\w+))?:\s"
                r"(\(\+?(?P<country_code>\d{1,3})\)\s)?"
                r"((?P<area_code>\d{3})-)?"
                r"(?P<exchange_code>\d{3})-"
                r"(?P<station_code>\d{4})",
            )
            match = pattern.search(line)
            if match:
                print(
                    f"HIT: Line {line_number}: "
                    f"surname: {match.group('surname')!r} | "
                    f"first name: {match.group('first_name')!r} | "
                    f"middle name: {match.group('middle_name')!r} | "
                    f"country code: {default_country_code(match)!r} | "
                    f"area code: {match.group('area_code')!r} | "
                    f"exchange code: {match.group('exchange_code')!r} | "
                    f"station code: {match.group('station_code')!r}",
                )
    print("=" * 40)


if __name__ == "__main__":
    main()
