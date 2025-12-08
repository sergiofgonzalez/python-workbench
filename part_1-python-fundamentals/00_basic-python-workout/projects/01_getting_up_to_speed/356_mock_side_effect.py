"""Customizing a Mock's behavior with .side_effect."""

# Uncomment the following imports to test the actual function
# import sys  # noqa: ERA001
# import requests  # noqa: ERA001
import logging
from unittest.mock import Mock

from requests.exceptions import Timeout

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

logger = logging.getLogger(__name__)

requests = Mock()


def get_holidays() -> dict[str, str] | None:
    """Return a dictionary of holidays (this actually works!)."""
    logger.debug("Retrieving holidays for 2025...")
    r = requests.get("https://date.nager.at/api/v3/PublicHolidays/2025/US", timeout=10)
    if r.status_code != 200:  # noqa: PLR2004
        logger.error("Failed to retrieve holidays: %d", r.status_code)
        return None
    holidays = r.json()
    logger.info("Retrieved %d holidays.", len(holidays))
    return {holiday["date"]: holiday["localName"] for holiday in holidays}


def main() -> None:
    """Application entry point."""

    # uncomment the following lines to test the actual function
    # holidays = get_holidays()  # noqa: ERA001
    # if holidays is None:
    #     print("Failed to retrieve holidays.")  # noqa: ERA001
    #     sys.exit(1)  # noqa: ERA001
    # print(f"Number of holidays in 2025: {len(holidays)}")  # noqa: ERA001
    # print(holidays)  # noqa: ERA001
    def get_holidays_side_effect(*args: str, **kwargs: str) -> dict[str, str]:
        """Mock get_holidays() with sample holiday data."""
        """Mock get_holidays() with sample holiday data."""
        logger.debug(
            "Mocking get_holidays_side_effect: args=%s, kwargs=%s",
            args,
            kwargs,
        )
        response_mock = Mock()
        response_mock.status_code = 200
        response_mock.json.return_value = [
            {"date": "2025-01-01", "localName": "New Year's Day"},
            {"date": "2025-07-04", "localName": "Independence Day"},
            {"date": "2025-12-25", "localName": "Christmas Day"},
        ]
        return response_mock

    # Testing the error path with a Timeout exception
    requests.get.side_effect = Timeout
    try:
        holidays = get_holidays()
    except Exception as exc:  # noqa: BLE001
        print(f"Exception as expected: {exc} (exception type: {type(exc).__name__})")
        print("== passed error path with mocked side_effect ==")

    # Testing the successful path with a side_effect function
    requests.get.side_effect = get_holidays_side_effect
    holidays = get_holidays()
    assert holidays is not None
    assert len(holidays) == 3  # noqa: PLR2004
    assert holidays["2025-07-04"] == "Independence Day"
    assert holidays["2025-12-25"] == "Christmas Day"
    assert holidays["2025-01-01"] == "New Year's Day"
    print("== passed with mocked side_effect ==")

    # We could have also performed the configuration of the side effect in one shot:
    requests.get.side_effect = [
        Timeout("Connection timed out!"),
        get_holidays_side_effect(),
    ]
    try:
        holidays = get_holidays()
    except Exception as exc:  # noqa: BLE001
        print(f"Exception as expected: {exc} (exception type: {type(exc).__name__})")
        print("== passed error path with mocked side_effect (2) ==")

    holidays = get_holidays()
    assert holidays is not None
    assert len(holidays) == 3  # noqa: PLR2004
    assert holidays["2025-07-04"] == "Independence Day"
    assert holidays["2025-12-25"] == "Christmas Day"
    assert holidays["2025-01-01"] == "New Year's Day"
    print("== passed with mocked side_effect (2) ==")


if __name__ == "__main__":
    main()
