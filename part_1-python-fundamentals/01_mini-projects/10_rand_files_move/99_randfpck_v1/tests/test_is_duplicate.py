"""is_duplicate function tests"""
import re
import unittest
from collections import namedtuple
from unittest.mock import MagicMock, patch

from randfpck.main import is_duplicate


class TestIsDuplicate(unittest.TestCase):
    """Test is_duplicate function features"""

    def test_is_duplicate(self):
        """is_duplicate function tests"""

        Subtest = namedtuple(
            "Subtest",
            ["file_size", "file_md5", "file_content", "file_sizes", "expected"],
        )

        subtests = {
            "single file empty folder": Subtest(
                file_size=100,
                file_md5="1234",
                file_content="abc",
                file_sizes={},
                expected=False,
            ),
            "single file failed size, same md5 and content": Subtest(
                file_size=100,
                file_md5="1234",
                file_content="abc",
                file_sizes={101: ["some-file-md5_1234-content_abc.txt"]},
                expected=False,
            ),
            "single file same size, failed md5 and content": Subtest(
                file_size=100,
                file_md5="1234",
                file_content="abc",
                file_sizes={100: ["some-file-md5_5555-content_abc.txt"]},
                expected=False,
            ),
            "single file same size, same md5 and failed content": Subtest(
                file_size=100,
                file_md5="1234",
                file_content="abc",
                file_sizes={100: ["some-file-md5_5555-content_xyz.txt"]},
                expected=False,
            ),
            "single file match": Subtest(
                file_size=100,
                file_md5="1234",
                file_content="abc",
                file_sizes={100: ["some-file-md5_1234-content_abc.txt"]},
                expected=True,
            ),
            "several files match": Subtest(
                file_size=100,
                file_md5="1234",
                file_content="abc",
                file_sizes={
                    100: [
                        "another-file-md5_555-content_xyz.md",
                        "some-file-md5_1234-content_abc.txt",
                    ]
                },
                expected=True,
            ),
            "several files non-match": Subtest(
                file_size=100,
                file_md5="1234",
                file_content="abc",
                file_sizes={
                    100: [
                        "another-file-md5_555-content_xyz.md",
                        "some-file-md5_1234-content_xyz.txt",
                    ]
                },
                expected=False,
            ),
        }

        def get_file_md5_side_fx(mock_file_path):
            """Mocks the get_file_md5 behavior"""
            return mock_file_path.md5

        def file_path_for_filename_fx(_, file):
            """Mocks the file_path_for_filename behavior"""
            # This is another code smell that the function under test is too
            # complex, but kept it as-is for reference
            match = re.search(r"md5_(\d+)-content_(\D+)\.", file)
            if not match:
                raise ValueError(
                    (
                        "naming convention file-md5_{md5}-content_{content}.ext"
                        " not fnd"
                    )
                )
            mock_fpath = MagicMock()
            mock_fpath.md5 = match.group(1)
            mock_fpath.content = match.group(2)
            return mock_fpath

        def cmp_side_fx(f1, f2, shallow):   # pylint: disable=unused-argument
            """Mocks the filecmp.cmp behavior"""
            return f1.content == f2.content

        for name, data in subtests.items():
            with (
                patch(
                    "randfpck.main.file_path_for_filename",
                    side_effect=file_path_for_filename_fx,
                ),
                patch(
                    "randfpck.main.FolderFiles.get_file_md5",
                    side_effect=get_file_md5_side_fx,
                ),
                patch("randfpck.main.filecmp.cmp", side_effect=cmp_side_fx),
            ):
                mock_file_path = MagicMock()
                mock_file_path.stat.return_value.st_size = data.file_size
                mock_file_path.md5 = data.file_md5
                mock_file_path.content = data.file_content
                mock_folder_files = MagicMock()
                mock_folder_files.file_sizes = data.file_sizes

                got = is_duplicate(mock_file_path, mock_folder_files)
                self.assertEqual(
                    got,
                    data.expected,
                    f"{name}: expected {data.expected} but got {got}",
                )
