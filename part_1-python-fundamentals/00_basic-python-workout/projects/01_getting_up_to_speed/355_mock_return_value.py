"""Customizing a Mock's return value."""

import logging
from datetime import UTC
from unittest.mock import Mock

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

datetime = Mock()


def is_weekday() -> bool:
    """Return True if today is a weekday, False otherwise."""
    # 0-4 are weekdays (Monday to Friday)
    today_ord = datetime.now(tz=UTC).weekday()
    logger.info("Today ordinal is %d", today_ord)
    return today_ord < 5  # noqa: PLR2004


def main() -> None:
    """Application entry point."""
    # You need to mock datetime.now().weekday() to test both branches

    # Weekday branch
    datetime.now().weekday.return_value = 2  # Wednesday
    print(f"Is it a weekday? {is_weekday()}")
    assert is_weekday() is True
    print("== passed for weekday ==")

    # Weekend branch
    datetime.now().weekday.return_value = 6  # Sunday
    print(f"Is it a weekday? {is_weekday()}")
    assert is_weekday() is False
    print("== passed for weekend ==")


if __name__ == "__main__":
    main()
