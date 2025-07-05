"""Illustrate parsing a string into a date."""

from datetime import UTC, datetime


def main() -> None:
    """Application entry point."""
    # Parsing "1974-02-05T14:05:18" into a timezone-aware datetime object
    my_dt = datetime.fromisoformat("1974-02-05T14:05:18+00:00")
    print(f"parsed {my_dt} (type: {type(my_dt)})")

    # Parsing 17/05/2008 23:15:47
    my_dt = datetime.strptime("17/05/2008 23:15:47", "%d/%m/%Y %H:%M:%S").replace(
        tzinfo=UTC,
    )
    print(f"parsed {my_dt} (type: {type(my_dt)})")


if __name__ == "__main__":
    main()
