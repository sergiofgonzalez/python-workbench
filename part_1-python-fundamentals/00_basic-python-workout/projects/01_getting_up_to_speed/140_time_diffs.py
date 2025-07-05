"""Illustrate how to compute time differences using timedelta."""

from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo


def get_date_n_days_after_today(n: int, tz: str = "UTC") -> date:
    """Return a date that is n days after today."""
    today = datetime.now(tz=ZoneInfo(tz)).date()
    return today + timedelta(days=n)


def get_date_n_days_ago(n: int, tz: str = "UTC") -> date:
    """Return a date that is n days ago from today."""
    today = datetime.now(tz=ZoneInfo(tz)).date()
    return today - timedelta(days=n)


def main() -> None:
    """Application entry point."""
    # Set the timezone for Madrid
    madrid_tz = ZoneInfo("Europe/Madrid")

    # Difference between now and a specific date
    now = datetime.now(tz=madrid_tz)
    specific_date = datetime(1974, 2, 5, tzinfo=madrid_tz)
    time_diff = now - specific_date
    print(f"Time difference between now and {specific_date}: {time_diff}")

    # Getting the number of days between those two dates
    days_diff = time_diff.days
    print(f"Number of days between now and {specific_date}: {days_diff:,} days")

    # Getting the number of seconds between those two dates
    seconds_diff = time_diff.total_seconds()
    print(
        f"Number of seconds between now and {specific_date}: {seconds_diff:,} seconds",
    )

    # Getting n days after today
    n = 10
    n_days_after_today = get_date_n_days_after_today(n, tz="Europe/Madrid")
    print(f"{n} days after today in Madrid: {n_days_after_today}")

    # Getting n days ago from today
    n = 10
    n_days_ago = get_date_n_days_ago(n, tz="Europe/Madrid")
    print(f"{n} days ago from today in Madrid: {n_days_ago}")

    # Getting how many days are left until my summer holidays
    today = datetime.now(tz=madrid_tz).date()
    summer_holidays = date(2025, 8, 4)
    days_until_summer_holidays = (summer_holidays - today).days
    print(
        f"Days until summer holidays on {summer_holidays}: "
        f"{days_until_summer_holidays} days",
    )


if __name__ == "__main__":
    main()
