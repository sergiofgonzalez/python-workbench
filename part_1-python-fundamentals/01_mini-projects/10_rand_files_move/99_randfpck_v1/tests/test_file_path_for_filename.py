"""file_path_for_filename function tests"""
import unittest
from pathlib import Path

from randfpck.main import file_path_for_filename


class TestFilePathForFilename(unittest.TestCase):
    """Test the file_path_for_filename features"""

    def test_file_path_for_filename_happy_path(self):
        """Test the happy path for file_path_for_filename function"""
        got = file_path_for_filename(Path("path/to/filename"), "filename1")
        expected = Path("path/to/filename/filename1")

        self.assertEqual(got, expected, f"expected {expected} but got {got}")

    def test_file_path_for_filename_unhappy_path(self):
        """Test the unhappy path for file_path_for_filename function"""

        with self.assertRaises(
            TypeError, msg="expected TypeError but found something different"
        ):
            file_path_for_filename("path/to/filename", "filename1")
