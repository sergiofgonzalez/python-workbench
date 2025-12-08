"""Illustrates how to use the patch decorator."""

import unittest
from unittest.mock import MagicMock, patch

import requests

import lib.cldr


class CalendarTestCase(unittest.TestCase):
    """Tests for calendar-related functionality."""

    @patch("lib.cldr.datetime")
    def test_is_weekday_for_weekday(self, mock_datetime: MagicMock) -> None:
        """Test for weekday detection."""
        mock_datetime.now.return_value.weekday.return_value = 2
        assert lib.cldr.is_weekday()

    @patch("lib.cldr.datetime")
    def test_is_weekday_for_weekend(self, mock_datetime: MagicMock) -> None:
        """Test for weekday detection."""
        mock_datetime.now.return_value.weekday.return_value = 5
        assert not lib.cldr.is_weekday()

    @patch("lib.cldr.requests.get")
    def test_get_holidays_success(self, mock_get: MagicMock) -> None:
        """Test for successful holiday retrieval."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {"date": "2025-01-01", "localName": "New Year's Day"},
            {"date": "2025-07-04", "localName": "Independence Day"},
        ]
        mock_get.return_value = mock_response

        holidays = lib.cldr.get_holidays()
        expected_holidays = {
            "2025-01-01": "New Year's Day",
            "2025-07-04": "Independence Day",
        }
        assert holidays == expected_holidays

    @patch("lib.cldr.requests.get")
    def test_get_holidays_error_500(self, mock_get: MagicMock) -> None:
        """Test for error in holiday retrieval."""
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response

        holidays = lib.cldr.get_holidays()
        assert holidays is None

    @patch("lib.cldr.requests")
    def test_get_holidays_error_timeout(self, mock_requests: MagicMock) -> None:
        """Test for error in holiday retrieval."""
        mock_requests.get.side_effect = requests.Timeout
        with self.assertRaises(requests.Timeout):  # noqa: PT027
            lib.cldr.get_holidays()
        mock_requests.get.assert_called_once()


if __name__ == "__main__":
    unittest.main()
