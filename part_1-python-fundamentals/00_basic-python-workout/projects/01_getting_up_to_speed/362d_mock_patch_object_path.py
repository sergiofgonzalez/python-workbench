"""Illustrates the nuances of identifying object path when using Mock.patch."""

import unittest
from unittest.mock import patch

# Case D: importing the library function directly
import lib


class CalendarTestCase(unittest.TestCase):
    """Tests for calendar-related functionality."""

    def test_is_weekday(self) -> None:
        """Test for weekday detection."""
        for day in range(7):
            with patch("lib.cldr.datetime") as mock_datetime:
                mock_datetime.now.return_value.weekday.return_value = day
                if day < 5:  # noqa: PLR2004
                    assert lib.cldr.is_weekday() # type: ignore  # noqa: PGH003
                else:
                    assert not lib.cldr.is_weekday() # type: ignore  # noqa: PGH003


if __name__ == "__main__":
    unittest.main()
