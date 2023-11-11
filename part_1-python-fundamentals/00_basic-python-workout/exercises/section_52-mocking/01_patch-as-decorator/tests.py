"""Test for my_calendar"""
import unittest
from unittest.mock import patch

from requests.exceptions import Timeout

from my_calendar import get_holidays


class TestCalendar(unittest.TestCase):
    """Test class for my_calendar module"""

    @patch("my_calendar.requests")
    def test_get_holidays_timeout(self, mock_requests):
        """Test timeout functionality in get_holidays function"""
        mock_requests.get.side_effect = Timeout
        with self.assertRaises(Timeout):
            get_holidays()
            mock_requests.get.assert_called_once()


if __name__ == "__main__":
    unittest.main()
