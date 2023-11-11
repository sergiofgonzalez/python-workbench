"""get_unique_filename function tests"""
import unittest
from collections import namedtuple
from pathlib import Path
from unittest.mock import MagicMock, patch

from randfpck.main import get_unique_filename


class TestGetUniqueFilename(unittest.TestCase):
    """Tests get_unique_filename function features"""

    def test_get_unique_filename(self):
        Subtest = namedtuple("Subtest", ["filename", "folders", "expected"])

        subtests = {
            "no clash, multiple folders": Subtest(
                filename="file1.txt",
                folders={
                    "folder1": ["file1.md", "file2.txt"],
                    "folder2": ["file1.log", "file2.md"],
                },
                expected="file1.txt",
            ),
            "one clash on first folder": Subtest(
                filename="file1.txt",
                folders={
                    "folder1": ["file1.txt", "file2.log"],
                    "folder2": ["file1.log", "file2.md"],
                },
                expected="file1.1.txt",
            ),
            "one clash on first folder, then on second": Subtest(
                filename="file1.txt",
                folders={
                    "folder1": ["file1.txt", "file2.log"],
                    "folder2": ["file1.log", "file1.1.txt"],
                },
                expected="file1.2.txt",
            ),
            "multiple clashes": Subtest(
                filename="file1.txt",
                folders={
                    "folder1": [
                        "file1.txt",
                        "file1.1.txt",
                        "other.txt",
                        "f.md",
                    ],
                    "folder2": [
                        "file1.2.txt",
                        "file1.3.txt",
                        "yes.txt",
                        "no.bin",
                    ],
                },
                expected="file1.4.txt",
            ),
        }

        def file_path_for_filename_side_fx(folder, filename):
            """Provides the stubbed behavior for file_path_for_filename.
            It checks whether the given filename is available in the subtest
            info provided.
            """
            exists_ret_value = filename in data.folders[folder]
            mock = MagicMock()
            mock.exists.return_value = exists_ret_value

            return mock

        for name, data in subtests.items():
            with patch(
                "randfpck.main.file_path_for_filename",
                side_effect=file_path_for_filename_side_fx,
            ):
                # Setup mock args
                mock_file_path = Path(data.filename)
                mock_folders_to_check = data.folders.keys()

                got = get_unique_filename(mock_file_path, mock_folders_to_check)
                self.assertEqual(
                    got,
                    data.expected,
                    f"{name}: expected {data.expected} but got {got}",
                )
