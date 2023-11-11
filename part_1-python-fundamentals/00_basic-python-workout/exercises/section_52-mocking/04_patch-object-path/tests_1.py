"""Test for my_calendar"""
import unittest
from unittest.mock import patch

import my_calendar


class TestCalendar(unittest.TestCase):
    """Test class for my_calendar module"""

    def test_weekday_mock(self):
        with patch("my_calendar.is_weekday"):
            my_calendar.is_weekday()
            print(f"my_calendar.is_weekday(): {my_calendar.is_weekday()}")


if __name__ == "__main__":
    unittest.main()
