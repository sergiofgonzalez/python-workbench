"""Illustrates how to use the patch context manager."""

import unittest
from unittest.mock import MagicMock, patch

import requests

import lib.cldr


class CalendarTestCase(unittest.TestCase):
    """Tests for calendar-related functionality."""

    def test_is_weekday(self) -> None:
        """Test for weekday detection."""
        for day in range(7):
            with patch("lib.cldr.datetime") as mock_datetime:
                mock_datetime.now.return_value.weekday.return_value = day
                if day < 5:  # noqa: PLR2004
                    assert lib.cldr.is_weekday()
                else:
                    assert not lib.cldr.is_weekday()

    def test_get_holidays_success(self) -> None:
        """Test for successful holiday retrieval."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {"date": "2025-01-01", "localName": "New Year's Day"},
            {"date": "2025-07-04", "localName": "Independence Day"},
        ]
        with patch("lib.cldr.requests.get", return_value=mock_response) as mock_get:
            holidays = lib.cldr.get_holidays()
            expected_holidays = {
                "2025-01-01": "New Year's Day",
                "2025-07-04": "Independence Day",
            }
            assert holidays == expected_holidays
            mock_get.assert_called_once()

    def test_get_holidays_error_500(self) -> None:
        """Test for error in holiday retrieval."""
        mock_response = MagicMock()
        mock_response.status_code = 500
        with patch("lib.cldr.requests.get", return_value=mock_response) as mock_get:
            holidays = lib.cldr.get_holidays()
            assert holidays is None
            mock_get.assert_called_once()


    def test_get_holidays_error_timeout(self) -> None:
        """Test for error in holiday retrieval."""
        with patch("lib.cldr.requests.get", side_effect=requests.Timeout) as mock_get:
            with self.assertRaises(requests.Timeout):  # noqa: PT027
                lib.cldr.get_holidays()
            mock_get.assert_called_once()


if __name__ == "__main__":
    unittest.main()
