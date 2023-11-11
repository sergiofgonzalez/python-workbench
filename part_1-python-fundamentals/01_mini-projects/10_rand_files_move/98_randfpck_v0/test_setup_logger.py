"""Testing setup_logger function"""
import logging
import unittest
from collections import namedtuple

from randfpck import setup_logger


class TestLoggerSetup(unittest.TestCase):
    """Test the setup_logger function"""

    def test_logger_level(self):
        """validates that the setup_logger returns a logger with the expected logger level"""
        logger = setup_logger()
        expected_level = logging.DEBUG
        self.assertEqual(
            logger.level, expected_level, f"expected {expected_level} but got {logger.level}"
        )

    def test_logger_handlers(self):
        """validates that the setup_logger returns a logger with the expected logger handlers"""
        logger = setup_logger()
        got_handlers = logger.handlers

        TestCase = namedtuple("TestCase", ["index", "expected_type", "expected_fmt_str", "expected_datefmt_str", "expected_level"])

        test_cases = {
            "console handler": TestCase(
                index=0,
                expected_type=logging.StreamHandler,
                expected_fmt_str="%(asctime)s.%(msecs)03d [%(levelname)8s] (%(name)s) | %(message)s",
                expected_datefmt_str="%Y-%m-%d %H:%M:%S",
                expected_level=logging.DEBUG
            ),
            "all_file_handler": TestCase(
                index=1,
                expected_type=logging.FileHandler,
                expected_fmt_str="%(asctime)s.%(msecs)03d [%(levelname)8s] (%(name)s) | %(message)s",
                expected_datefmt_str="%Y-%m-%d %H:%M:%S",
                expected_level=logging.DEBUG
            ),
            "error_file_handler": TestCase(
                index=2,
                expected_type=logging.FileHandler,
                expected_fmt_str="%(asctime)s.%(msecs)03d [%(levelname)8s] (%(name)s) | %(message)s",
                expected_datefmt_str="%Y-%m-%d %H:%M:%S",
                expected_level=logging.WARNING
            )
        }

        for test_case, test_data in test_cases.items():
            got_handler = got_handlers[test_data.index]
            got_handler_fmt_str = got_handler.formatter._fmt  # pylint: disable=protected-access
            got_handler_datefmt_str = got_handler.formatter.datefmt
            got_handler_level = got_handler.level

            self.assertIsInstance(
                got_handler,
                test_data.expected_type,
                f"{test_case}: got {type(got_handlers)}, but expected {test_data.expected_type}",
            )

            self.assertEqual(
                got_handler_fmt_str,
                test_data.expected_fmt_str,
                f"{test_case}: got {got_handler_fmt_str} but expected {test_data.expected_fmt_str}",  # pylint: disable=line-too-long
            )

            self.assertEqual(
                got_handler_datefmt_str,
                test_data.expected_datefmt_str,
                f"{test_case}: got {got_handler_datefmt_str} but expected {test_data.expected_datefmt_str}",  # pylint: disable=line-too-long
            )

            self.assertEqual(
                got_handler_level,
                test_data.expected_level,
                f"{test_case}: got {got_handler_level} but expected {test_data.expected_level}",
            )


if __name__ == "__main__":
    unittest.main()
