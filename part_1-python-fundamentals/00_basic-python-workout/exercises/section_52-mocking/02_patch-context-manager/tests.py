"""Test for my_calendar"""
import unittest
from unittest.mock import patch

from requests.exceptions import Timeout

from my_calendar import get_holidays


class TestCalendar(unittest.TestCase):
    """Test class for my_calendar module"""

    def test_get_holidays_timeout(self):
        """Test timeout functionality in get_holidays function"""
        with patch("my_calendar.requests") as mock_requests:
            mock_requests.get.side_effect = Timeout
            with self.assertRaises(Timeout):
                get_holidays()
                mock_requests.get.assert_called_once()


if __name__ == "__main__":
    unittest.main()
