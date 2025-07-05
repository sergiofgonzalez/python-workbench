"""Illustrate the basics of datetime package."""

from datetime import UTC, datetime, time


def main() -> None:
    """Application entry point."""
    # Getting the current date (without time), using UTC timezone
    current_date = datetime.now(tz=UTC).date()
    print(f"Current date: {current_date}")

    # Getting the current time (without date), using UTC timezone
    current_time = datetime.now(tz=UTC).time()
    print(f"Currrent time: {current_time}")

    # Create a variable holding the first day of 2025
    my_date = datetime(2025, 1, 1, tzinfo=UTC).date()
    print(f"First day of 2025: {my_date}")

    # Create a variable that holds noon's time
    noon = time(12, 0, 0, tzinfo=UTC)
    print(f"Noon: {noon}")

    # Create a variable holding 1974-02-05T14:05:48
    my_dt = datetime(1974, 2, 5, 14, 5, 48, tzinfo=UTC)
    print(f"Birth date: {my_dt}")

    # Trying to subtract noon from today's date raises
    try:
        my_date = current_date - noon  # type: ignore  # noqa: PGH003
    except Exception as e:  # noqa: BLE001
        print(f"{e} (exception type: {type(e)})")

    # Converting a date to a datetime using datetime()
    my_datetime = datetime(my_date.year, my_date.month, my_date.day, tzinfo=UTC)
    print(f"Converted date to datetime: {my_datetime}")

    # Combine a date and time using datetime.combine()
    my_datetime = datetime.combine(my_date, current_time, tzinfo=UTC)
    print(f"Combining a date and a time: {my_datetime}")


if __name__ == "__main__":
    main()
