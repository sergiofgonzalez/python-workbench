"""Testing UserOptions class"""
import unittest
from collections import namedtuple
from pathlib import Path
from unittest.mock import mock_open, patch

from randfpck.main import FolderFiles


class TestFolderFiles(unittest.TestCase):
    """Test the FolderFiles class features"""

    @patch("builtins.open", new_callable=mock_open, read_data=b"Hello, world!")
    def test_get_file_md5(self, mocked_open):
        """Checks that the md5 file returns the corresponding hash for a file"""
        got = FolderFiles.get_file_md5("path/to/file")
        expected = "6cd3556deb0da54bca060b4c39479839"
        self.assertEqual(got, expected, f"got {got} but expected {expected}")
        self.assertEqual(
            mocked_open.call_count,
            1,
            f"expected open() to be called once, but was called {mocked_open.call_count} times",  # pylint: disable=line-too-long
        )
        self.assertTupleEqual(
            mocked_open.call_args.args, ("path/to/file", "rb")
        )

    def test_folder_files_ctor_folder(self):
        """Tests the folder attribute when using the FolderFiles constructor"""

        SubTest = namedtuple("SubTest", ["folder", "expected_folder"])

        sub_tests = {
            "str as folder": SubTest(
                folder="path/to/folder", expected_folder=Path("path/to/folder")
            ),
            "Path as folder": SubTest(
                folder=Path("path/to/folder"),
                expected_folder=Path("path/to/folder"),
            ),
        }

        for subtest_name, subtest_data in sub_tests.items():
            got = FolderFiles(subtest_data.folder)
            expected_folder = subtest_data.expected_folder
            self.assertEqual(
                got.folder,
                expected_folder,
                (
                    f"{subtest_name}: expected {expected_folder} "
                    f"but got {got.folder}"
                ),
            )

    def test_folder_files_ctor_patterns(self):
        """Tests the glob patterns attribute when using the FolderFiles
        constructor
        """

        # pass nothing as glob patterns
        got = FolderFiles("path/to/folder")
        expected_glob_patterns = ["*"]
        self.assertEqual(
            got.glob_patterns,
            expected_glob_patterns,
            f"expected {expected_glob_patterns} but got {got.glob_patterns}",
        )

        SubTest = namedtuple(
            "SubTest", ["glob_patterns", "expected_glob_patterns"]
        )
        subtests = {
            "list with single element": SubTest(
                glob_patterns=["*.txt"], expected_glob_patterns=["*.txt"]
            ),
            "list with multiple elements": SubTest(
                glob_patterns=["*.txt", "*.md"],
                expected_glob_patterns=["*.txt", "*.md"],
            ),
        }

        for subtest_name, subtest_data in subtests.items():
            got = FolderFiles(
                "path/to/folder", glob_patterns=subtest_data.glob_patterns
            )
            self.assertEqual(
                got.glob_patterns,
                subtest_data.expected_glob_patterns,
                (
                    f"{subtest_name}: "
                    f"expected {subtest_data.expected_glob_patterns} "
                    f"but got {got.glob_patterns}"
                ),
            )

    def test_folder_files_ctor_file_sizes(self):
        """Tests the glob patterns attribute when using the FolderFiles
        constructor
        """

        # build metadata with multiple files several sizes
        def side_fx_mock_file_path_for_filename(_, filename):
            """This simple function will return variable responses when the
            the mocked file_path_for_filename function is called.
            The strategy used is to return the filename
            """
            return filename

        def mock_get_file_size_side_fx(file_path):
            """This simple function will return variable responses when the
            mocked get_file_size function is called.
            The strategy used is to return the last character of the filename
            as the size, which means that the files fed to this function must
            contain a number as the last char.
            """
            return int(file_path[-1])

        # not sending build_metadata arg
        got = FolderFiles("path/to/file")
        expected_file_sizes = dict()
        self.assertEqual(
            got.file_sizes,
            expected_file_sizes,
            (f"expected {expected_file_sizes} but got {got.file_sizes}"),
        )

        Subtest = namedtuple("Subtest", ["files", "expected", "build_metadata"])

        subtest = {
            "build_metadata set to False": Subtest(
                build_metadata=False, files=None, expected=dict()
            ),
            "empty file list": Subtest(
                build_metadata=True, files=[], expected=dict()
            ),
            "single file": Subtest(
                build_metadata=True,
                files=["file1-5"],
                expected={5: ["file1-5"]},
            ),
            "multiple files all same size": Subtest(
                build_metadata=True,
                files=["file1-1", "file2-1"],
                expected={1: ["file1-1", "file2-1"]},
            ),
            "multiple files all different sizes": Subtest(
                build_metadata=True,
                files=["file1-1", "file2-2"],
                expected={1: ["file1-1"], 2: ["file2-2"]},
            ),
            "multiple files with several sizes": Subtest(
                build_metadata=True,
                files=[
                    "file1-5",
                    "file2-3",
                    "file3-5",
                    "file4-3",
                    "file5-1",
                ],
                expected={
                    5: ["file1-5", "file3-5"],
                    3: ["file2-3", "file4-3"],
                    1: ["file5-1"],
                },
            ),
        }
        for subtest_name, subtest_data in subtest.items():
            with (
                patch(
                    "randfpck.main.find_files_matching",
                    return_value=subtest_data.files,
                ),
                patch(
                    "randfpck.main.file_path_for_filename",
                    side_effect=side_fx_mock_file_path_for_filename,
                ),
                patch(
                    "randfpck.main.get_file_size",
                    side_effect=mock_get_file_size_side_fx,
                ),
            ):
                got = FolderFiles(
                    "path/to/folder", build_metadata=subtest_data.build_metadata
                )

                self.assertDictEqual(
                    got.file_sizes,
                    subtest_data.expected,
                    (
                        f"{subtest_name}: "
                        f"expected {subtest_data.expected} "
                        f"but got {got.file_sizes}"
                    ),
                )

    def test_str(self):
        Subtest = namedtuple(
            "Subtest",
            ["folder", "files", "glob_patterns", "file_sizes", "expected"],
        )

        subtests = {
            "empty files, no metadata": Subtest(
                folder="path/to/folder",
                files=[],
                glob_patterns=["*"],
                file_sizes=dict(),
                expected=(
                    "folder=path/to/folder, patterns=['*'], "
                    "files=[], file_sizes={}"
                ),
            ),
            "several glob patterns": Subtest(
                folder="path/to/folder",
                files=[],
                glob_patterns=["*.txt", "*.md"],
                file_sizes=dict(),
                expected=(
                    "folder=path/to/folder, patterns=['*.txt', '*.md'], "
                    "files=[], file_sizes={}"
                ),
            ),
            "several files": Subtest(
                folder="path/to/folder",
                files=["file1.txt", "file2.txt"],
                glob_patterns=["*"],
                file_sizes=dict(),
                expected=(
                    "folder=path/to/folder, patterns=['*'], "
                    "files=file1.txt\nfile2.txt, file_sizes={}"
                ),
            ),
            "several file sizes": Subtest(
                folder="path/to/folder",
                files=["file1.txt", "file2.txt"],
                glob_patterns=["*"],
                file_sizes={
                    100: ["file1.txt"],
                    200: ["file21.txt", "file22.txt"],
                },
                expected=(
                    "folder=path/to/folder, patterns=['*'], "
                    "files=file1.txt\nfile2.txt, "
                    "file_sizes={100: ['file1.txt'], "
                    "200: ['file21.txt', 'file22.txt']}"
                ),
            ),
        }

        for subtest_name, subtest_data in subtests.items():
            with patch.object(FolderFiles, "__init__", return_value=None):
                mock_folder_files = FolderFiles(folder=subtest_data.folder)
                mock_folder_files.folder = subtest_data.folder
                mock_folder_files.files = subtest_data.files
                mock_folder_files.glob_patterns = subtest_data.glob_patterns
                mock_folder_files.file_sizes = subtest_data.file_sizes

                got = str(mock_folder_files)

                self.assertEqual(
                    got,
                    subtest_data.expected,
                    (
                        f"{subtest_name}: expected {subtest_data.expected} "
                        f"but got {got}"
                    ),
                )

    def test_repr(self):
        Subtest = namedtuple(
            "Subtest",
            ["folder", "files", "glob_patterns", "file_sizes", "expected"],
        )

        subtests = {
            "empty files, no metadata": Subtest(
                folder="path/to/folder",
                files=[],
                glob_patterns=["*"],
                file_sizes=dict(),
                expected=(
                    "FolderFiles(folder=path/to/folder, glob_patterns=['*'], "
                    "files=[], file_sizes={})"
                ),
            ),
            "several glob patterns": Subtest(
                folder="path/to/folder",
                files=[],
                glob_patterns=["*.txt", "*.md"],
                file_sizes=dict(),
                expected=(
                    "FolderFiles(folder=path/to/folder, "
                    "glob_patterns=['*.txt', '*.md'], "
                    "files=[], file_sizes={})"
                ),
            ),
            "several files": Subtest(
                folder="path/to/folder",
                files=["file1.txt", "file2.txt"],
                glob_patterns=["*"],
                file_sizes=dict(),
                expected=(
                    "FolderFiles(folder=path/to/folder, glob_patterns=['*'], "
                    "files=['file1.txt', 'file2.txt'], file_sizes={})"
                ),
            ),
            "several file sizes": Subtest(
                folder="path/to/folder",
                files=["file1.txt", "file2.txt"],
                glob_patterns=["*"],
                file_sizes={
                    100: ["file1.txt"],
                    200: ["file21.txt", "file22.txt"],
                },
                expected=(
                    "FolderFiles(folder=path/to/folder, glob_patterns=['*'], "
                    "files=['file1.txt', 'file2.txt'], "
                    "file_sizes={100: ['file1.txt'], "
                    "200: ['file21.txt', 'file22.txt']})"
                ),
            ),
        }

        for subtest_name, subtest_data in subtests.items():
            with patch.object(FolderFiles, "__init__", return_value=None):
                mock_folder_files = FolderFiles(folder=subtest_data.folder)
                mock_folder_files.folder = subtest_data.folder
                mock_folder_files.files = subtest_data.files
                mock_folder_files.glob_patterns = subtest_data.glob_patterns
                mock_folder_files.file_sizes = subtest_data.file_sizes

                got = repr(mock_folder_files)

                self.assertEqual(
                    got,
                    subtest_data.expected,
                    (
                        f"{subtest_name}: expected {subtest_data.expected} "
                        f"but got {got}"
                    ),
                )


if __name__ == "__main__":
    unittest.main()
