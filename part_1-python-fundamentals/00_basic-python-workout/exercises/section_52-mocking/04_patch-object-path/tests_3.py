"""Test for my_calendar"""
import unittest
from unittest.mock import patch

from my_calendar import is_weekday


class TestCalendar(unittest.TestCase):
    """Test class for my_calendar module"""

    def test_weekday_mock(self):
        """Test object has been effectively mocked"""
        with patch("__main__.is_weekday"):
            is_weekday()
            print(f"is_weekday(): {is_weekday()}")  # a mock!!!


if __name__ == "__main__":
    unittest.main()
