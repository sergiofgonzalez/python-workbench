"""Illustrate how to create timezone-aware datetime objects."""

from datetime import UTC, datetime, timedelta, timezone


def main() -> None:
    """Application entry point."""
    # Building a timezone-aware datetime object using the tzinfo argument as CEST+2
    cest = timezone(timedelta(hours=2), name="CEST")
    my_dt = datetime(2025, 7, 5, 8, 58, 0, tzinfo=cest)
    print(f"my_dt: {my_dt} (type: {type(my_dt)})")

    # Getting the current datetime in CEST
    now_cest = datetime.now(tz=cest)
    print(f"Current datetime in CEST: {now_cest}")

    # Getting the current datetime in UTC
    now_utc = datetime.now(tz=UTC)
    print(f"Current datetime in UTC: {now_utc}")

    # Creating a named timezone using the tzname argument
    madrid_tz = timezone(timedelta(hours=2), name="Europe/Madrid")
    now_madrid = datetime.now(tz=madrid_tz)
    print(f"Current datetime in Madrid: {now_madrid} (tzname: {now_madrid.tzname()})")


if __name__ == "__main__":
    main()
