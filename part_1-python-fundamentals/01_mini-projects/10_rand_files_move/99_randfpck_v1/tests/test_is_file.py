"""is_file function tests"""
import unittest
from collections import namedtuple
from unittest.mock import MagicMock

from randfpck.main import is_file


class TestIsFile(unittest.TestCase):
    """Test the is_file features"""

    def test_is_file(self):
        """Test the is_file function"""

        TestCase = namedtuple("TestCase", ["is_dir", "is_symlink", "expected"])

        test_cases = {
            "is dir": TestCase(is_dir=True, is_symlink=False, expected=False),
            "is symlink": TestCase(
                is_dir=False, is_symlink=True, expected=False
            ),
            "is both dir and symlink": TestCase(
                is_dir=True, is_symlink=True, expected=False
            ),
            "is neither dir nor symlink": TestCase(
                is_dir=False, is_symlink=False, expected=True
            ),
        }

        for test_case, test_data in test_cases.items():
            mock_file_path = MagicMock()
            mock_file_path.is_dir.return_value = test_data.is_dir
            mock_file_path.is_symlink.return_value = test_data.is_symlink
            got = is_file(mock_file_path)
            self.assertEqual(
                got,
                test_data.expected,
                f"{test_case}: expected {test_data.expected} but got {got}",
            )
