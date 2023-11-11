"""get_file_size function tests"""
import unittest
from unittest.mock import MagicMock, patch

from randfpck.main import get_file_size


class TestFileGetFileSize(unittest.TestCase):
    """Test the file_path_for_filename features"""

    def test_get_file_size_value(self):
        """Test get_file_size function"""
        mock_file_path = MagicMock()
        mock_file_path.stat.return_value.st_size = 100

        with patch("randfpck.main.is_file", return_value=True):
            got = get_file_size(mock_file_path)
            expected = 100

            self.assertEqual(
                got, expected, f"expected {expected} but got {got}"
            )

    def test_get_file_size_none(self):
        """Test get_file_size function"""
        mock_file_path = MagicMock()

        with patch("randfpck.main.is_file", return_value=False):
            got = get_file_size(mock_file_path)

            self.assertIsNone(got, f"expected None but got {got}")
