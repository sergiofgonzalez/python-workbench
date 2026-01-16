"""Illustrates how to build a phone number normalizer."""

import re
from pathlib import Path

base_path = Path("data", "in_data", "regex_files")


def normalize_phone_number(phone_number: str) -> str:
    """Take a US/Canada phone number and normalize it using regex."""
    pattern = (
        r"(\(?\+?(?P<country_code>1)\)?[\s-])?"
        r"\(?((?P<area_code>\d{3})\)?[\.\s-])?"
        r"(?P<exchange_code>\d{3})[\.\s-]"
        r"(?P<station_code>\d{4})"
    )

    match = re.match(pattern, phone_number)
    if match:
        if not (country_code := match.group("country_code")):
            country_code = 1
        return f"{country_code}-{match.group('area_code')}-{match.group('exchange_code')}-{match.group('station_code')}"  # noqa: E501
    return f"(no match) original was: {phone_number}"


def main() -> None:
    """Application entry point."""
    file_path = base_path / "06_textfile.txt"

    # peeking into the file to see how escape sequences are represented
    with file_path.open("r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            print(f"Line {line_number}: {line.strip()} (repr: {line!r})")
    print("=" * 40)

    # normalizing phone numbers in the file
    with file_path.open("r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            pattern = re.compile(
                r"(\(?\+?(?P<country_code>1)\)?[\s-])?"
                r"\(?((?P<area_code>\d{3})\)?[\.\s-])?"
                r"(?P<exchange_code>\d{3})[\.\s-]"
                r"(?P<station_code>\d{4})",
            )
            match = pattern.search(line)
            if match:
                print(
                    f"HIT: Line {line_number}: "
                    f"country code: {match.group('country_code')!r} | "
                    f"area code: {match.group('area_code')!r} | "
                    f"exchange code: {match.group('exchange_code')!r} | "
                    f"station code: {match.group('station_code')!r}",
                )
    print("=" * 40)

    # Now that everything matches, we can normalize
    with file_path.open("r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            print(
                f"{line_number}: {line.strip()} => "
                f"{normalize_phone_number(line.strip())}",
            )
    print("=" * 40)

    # bonus
    with file_path.open("r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            pattern = re.compile(
                r"(\(?\+?(?P<country_code>1)\)?[\s-])?"
                r"\(?((?P<area_code>[2-9][0-8]\d)\)?[\.\s-])?"
                r"(?P<exchange_code>[2-9]\d{2})[\.\s-]"
                r"(?P<station_code>\d{4})",
            )
            match = pattern.search(line)
            if match:
                print(
                    f"HIT: Line {line_number}: "
                    f"country code: {match.group('country_code')!r} | "
                    f"area code: {match.group('area_code')!r} | "
                    f"exchange code: {match.group('exchange_code')!r} | "
                    f"station code: {match.group('station_code')!r}",
                )
    print("=" * 40)


if __name__ == "__main__":
    main()
