"""Illustrates the nuances of identifying object path when using Mock.patch."""

import unittest
from datetime import UTC, datetime
from unittest.mock import patch

# Case E: mocking a function defined inline


def is_weekday() -> bool:
    """Return True if today is a weekday, False otherwise."""
    today_ord = datetime.now(tz=UTC).weekday()
    return today_ord < 5  # noqa: PLR2004


class CalendarTestCase(unittest.TestCase):
    """Tests for calendar-related functionality."""

    def test_is_weekday(self) -> None:
        """Test for weekday detection."""
        for day in range(7):
            with patch("__main__.datetime") as mock_datetime:
                mock_datetime.now.return_value.weekday.return_value = day
                if day < 5:  # noqa: PLR2004
                    assert is_weekday()
                else:
                    assert not is_weekday()

    def test_mock_weekday(self) -> None:
        """Test for weekday detection."""
        with patch("__main__.is_weekday") as mock_is_weekday:
            mock_is_weekday.return_value = True
            assert is_weekday()
            mock_is_weekday.return_value = False
            assert not is_weekday()


if __name__ == "__main__":
    unittest.main()
