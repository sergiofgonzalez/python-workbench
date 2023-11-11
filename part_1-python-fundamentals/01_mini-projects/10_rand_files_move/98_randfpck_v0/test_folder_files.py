"""Testing UserOptions class"""
import unittest
from collections import namedtuple
from pathlib import Path
from unittest.mock import MagicMock, Mock, mock_open, patch

from randfpck import FolderFiles


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

    def test_folder_files_constructor_no_metadata(self):
        """Checks the FolderFiles object construction when build_metadata=False.
        The glob library is mocked.
        """
        TestCase = namedtuple(
            "TestCase",
            [
                "folder",
                "files",
                "glob_patterns",
                "expected_folder",
                "expected_glob_patterns",
                "expected_file_sizes",
            ],
        )
        test_cases = {
            "empty glob": TestCase(
                folder=Path("path/to/folder"),
                glob_patterns=None,
                files=["file1", "file2", "file3"],
                expected_glob_patterns=["*"],
                expected_folder=Path("path/to/folder"),
                expected_file_sizes=dict(),
            ),
            "empty files returned": TestCase(
                folder=Path("path/to/folder"),
                glob_patterns=None,
                files=[],
                expected_folder=Path("path/to/folder"),
                expected_glob_patterns=["*"],
                expected_file_sizes=dict(),
            ),
            "multiple patterns": TestCase(
                folder=Path("path/to/folder"),
                glob_patterns=["*1", "*2", "*3"],
                files=["file1"],
                expected_folder=Path("path/to/folder"),
                expected_glob_patterns=["*1", "*2", "*3"],
                expected_file_sizes=dict(),
            ),
            "passing string in folder": TestCase(
                folder="path/to/folder",
                glob_patterns=["*1", "*2", "*3"],
                files=["file1"],
                expected_folder=Path("path/to/folder"),
                expected_glob_patterns=["*1", "*2", "*3"],
                expected_file_sizes=dict(),
            ),
        }

        for test_case, test_data in test_cases.items():
            with patch("randfpck.glob") as mock_glob:
                expected_files = (
                    [
                        f
                        for f in test_data.files
                        for _ in range(0, len(test_data.glob_patterns))
                    ]
                    if test_data.glob_patterns
                    else test_data.files
                )
                expected_folder = test_data.expected_folder
                expected_glob_patterns = test_data.expected_glob_patterns
                expected_file_sizes = test_data.expected_file_sizes

                mock_glob.glob.return_value = test_data.files
                if test_data.glob_patterns:
                    got = FolderFiles(
                        test_data.folder, glob_patterns=test_data.glob_patterns
                    )
                else:
                    got = FolderFiles(test_data.folder)
                self.assertListEqual(
                    got.files,
                    expected_files,
                    (
                        f"{test_case}: expected files to be {expected_files} "
                        f"but got {got.files}"
                    ),
                )
                self.assertEqual(
                    got.folder,
                    expected_folder,
                    (
                        f"{test_case}: expected folder to be {expected_folder} "
                        f"but was {got.folder}"
                    ),
                )
                self.assertTrue(
                    isinstance(got.folder, Path),
                    (
                        f"{test_case}: expected folder type to be Path "
                        f"but was {got.folder}"
                    ),
                )
                self.assertListEqual(
                    got.glob_patterns,
                    expected_glob_patterns,
                    (
                        f"{test_case}: expected glob_patterns to be "
                        f"{expected_glob_patterns} but was {got.glob_patterns}"
                    ),
                )
                self.assertDictEqual(
                    got.file_sizes,
                    expected_file_sizes,
                    (
                        f"{test_case}: expected file_sizes to be "
                        f"{expected_file_sizes} but was {got.file_sizes}"
                    ),
                )
                self.assertEqual(
                    mock_glob.glob.call_count,
                    len(expected_glob_patterns),
                    (
                        f"{test_case}: expected glob call_count to be "
                        f"{len(expected_glob_patterns)} but was "
                        f"{mock_glob.glob.call_count}"
                    ),
                )

    def test_folder_files_constructor_metadata(self):
        """Checks the FolderFiles._build_file_sizes_dicts which is invoked upon
        object construction when build_metadata=True.
        """
        TestData = namedtuple("TestData", ["folder files expected_file_sizes config"])

        # build metadata with empty files
        with patch.object(FolderFiles, "__init__", return_value=None):
            mock_folder_files = FolderFiles(folder="path/to/folder")
            mock_folder_files.files = []
            mock_folder_files.folder = "path/to/folder"
            mock_folder_files.file_sizes = dict()

            mock_folder_files._build_file_sizes_dict()  # pylint: disable=protected-access
            expected_dict = {}
            self.assertDictEqual(
                mock_folder_files.file_sizes,
                expected_dict,
                (
                    f"expected file sizes to be {expected_dict} "
                    f"but was {mock_folder_files.file_sizes}"
                ),
            )

        # build metadata with one entry, being a dir
        with patch.object(FolderFiles, "__init__", return_value=None):
            mock_folder_files = FolderFiles(folder="path/to/folder")
            mock_folder_files.files = ["file1"]
            mock_folder_files.folder = "path/to/folder"
            mock_folder_files.file_sizes = dict()

            # This is ugly as hell but works... smells like FolderFiles follows
            # a bad design and requires refactoring: it's doing too many things!
            # Another code smell is that we need to test and mock protected
            # functions
            mock_folder_files._get_file_path = (  # pylint: disable=protected-access
                MagicMock()
            )
            mock_folder_files._get_file_path.return_value.is_dir.return_value = (  # pylint: disable=protected-access,line-too-long
                True
            )

            mock_folder_files._build_file_sizes_dict()  # pylint: disable=protected-access
            expected_dict = {}
            self.assertDictEqual(
                mock_folder_files.file_sizes,
                expected_dict,
                (
                    f"expected file sizes to be {expected_dict} "
                    f"but was {mock_folder_files.file_sizes}"
                ),
            )

        # build metadata with one entry, being a symbolic link
        with patch.object(FolderFiles, "__init__", return_value=None):
            mock_folder_files = FolderFiles(folder="path/to/folder")
            mock_folder_files.files = ["file1"]
            mock_folder_files.folder = "path/to/folder"
            mock_folder_files.file_sizes = dict()

            # This is ugly as hell but works... smells like FolderFiles follows
            # a bad design and requires refactoring: it's doing too many things!
            # Another code smell is that we need to test and mock protected
            # functions
            mock_folder_files._get_file_path = (  # pylint: disable=protected-access
                MagicMock()
            )
            mock_folder_files._get_file_path.return_value.is_dir.return_value = (  # pylint: disable=protected-access,line-too-long
                False
            )
            mock_folder_files._get_file_path.return_value.is_symlink.return_value = (  # pylint: disable=protected-access,line-too-long
                True
            )

            mock_folder_files._build_file_sizes_dict()  # pylint: disable=protected-access
            expected_dict = {}
            self.assertDictEqual(
                mock_folder_files.file_sizes,
                expected_dict,
                (
                    f"expected file sizes to be {expected_dict} "
                    f"but was {mock_folder_files.file_sizes}"
                ),
            )

        # build metadata with one entry, being regular file so dict created
        with patch.object(FolderFiles, "__init__", return_value=None):
            mock_folder_files = FolderFiles(folder="path/to/folder")
            mock_folder_files.files = ["file1"]
            mock_folder_files.folder = "path/to/folder"
            mock_folder_files.file_sizes = dict()

            # This is ugly as hell but works... smells like FolderFiles follows
            # a bad design and requires refactoring: it's doing too many things!
            # Another code smell is that we need to test and mock protected
            # functions
            mock_folder_files._get_file_path = (  # pylint: disable=protected-access
                MagicMock()
            )
            mock_folder_files._get_file_path.return_value.is_dir.return_value = (  # pylint: disable=protected-access,line-too-long
                False
            )
            mock_folder_files._get_file_path.return_value.is_symlink.return_value = (  # pylint: disable=protected-access,line-too-long
                False
            )
            mock_folder_files._get_file_path.return_value.stat.return_value.st_size = (  # pylint: disable=protected-access,line-too-long
                100
            )

            mock_folder_files._build_file_sizes_dict()  # pylint: disable=protected-access
            expected_dict = {100: ["file1"]}
            self.assertDictEqual(
                mock_folder_files.file_sizes,
                expected_dict,
                (
                    f"expected file sizes to be {expected_dict} "
                    f"but was {mock_folder_files.file_sizes}"
                ),
            )

        # build metadata with two entries, first is a dir, second is a symlink
        with patch.object(FolderFiles, "__init__", return_value=None):
            mock_folder_files = FolderFiles(folder="path/to/folder")
            mock_folder_files.files = ["dir1", "symlink1"]
            mock_folder_files.folder = "path/to/folder"
            mock_folder_files.file_sizes = dict()

            # This is ugly as hell but works... smells like FolderFiles follows
            # a bad design and requires refactoring: it's doing too many things!
            # Another code smell is that we need to test and mock protected
            # functions
            mock_folder_files._get_file_path = (  # pylint: disable=protected-access
                MagicMock()
            )
            true_response_mock = MagicMock()
            true_response_mock.return_value = True
            false_response_mock = MagicMock()
            false_response_mock.return_value = False

            def my_side_fx(filename):
                if filename == "dir1":
                    mock = MagicMock(name="path for dir1")
                    mock.is_dir.return_value = True
                    mock.is_symlink.return_value = False
                    return mock
                elif filename == "symlink1":
                    mock = MagicMock(name="path for symlink1")
                    mock.is_dir.return_value = False
                    mock.is_symlink.return_value = True
                    return mock

            mock_folder_files._get_file_path.side_effect = (  # pylint: disable=protected-access
                my_side_fx
            )

            mock_folder_files._build_file_sizes_dict()  # pylint: disable=protected-access
            expected_dict = {}
            self.assertDictEqual(
                mock_folder_files.file_sizes,
                expected_dict,
                (
                    f"expected file sizes to be {expected_dict} "
                    f"but was {mock_folder_files.file_sizes}"
                ),
            )

        # build metadata with two entries, first is a dir, second is a file
        with patch.object(FolderFiles, "__init__", return_value=None):
            mock_folder_files = FolderFiles(folder="path/to/folder")
            mock_folder_files.files = ["dir1", "symlink1"]
            mock_folder_files.folder = "path/to/folder"
            mock_folder_files.file_sizes = dict()

            # This is ugly as hell but works... smells like FolderFiles follows
            # a bad design and requires refactoring: it's doing too many things!
            # Another code smell is that we need to test and mock protected
            # functions
            mock_folder_files._get_file_path = (  # pylint: disable=protected-access
                MagicMock()
            )
            true_response_mock = MagicMock()
            true_response_mock.return_value = True
            false_response_mock = MagicMock()
            false_response_mock.return_value = False

            def my_side_fx(filename):
                if filename == "dir1":
                    mock = MagicMock(name="path for dir1")
                    mock.is_dir.return_value = True
                    mock.is_symlink.return_value = False
                    return mock
                elif filename == "symlink1":
                    mock = MagicMock(name="path for symlink1")
                    mock.is_dir.return_value = False
                    mock.is_symlink.return_value = True
                    return mock

            mock_folder_files._get_file_path.side_effect = (  # pylint: disable=protected-access
                my_side_fx
            )

            mock_folder_files._build_file_sizes_dict()  # pylint: disable=protected-access
            expected_dict = {}
            self.assertDictEqual(
                mock_folder_files.file_sizes,
                expected_dict,
                (
                    f"expected file sizes to be {expected_dict} "
                    f"but was {mock_folder_files.file_sizes}"
                ),
            )

        # build metadata with one entry on files, being dir
        # build metadata with one entry on files, being symlink
        # build metadata with two entries: dir + symlink
        # build metadata with two entries: dir + file
        # build metadata with two entries: symlink + file
        # build metadata with two entries: file + file, diff sizes
        # build metadata with two entries: file + file, same sizes
        # build metadata with three entries: file + file, same sizes, file diff size

        # checking the metadata build with and without files, multiple files, etc.

        # MockArgs = namedtuple("MockArgs", ["src", "dst", "used", "num_files", "glob"])
        # mock_args = MockArgs(src="src/", dst="dst/", used="used/", num_files=5, glob=["glob.*"])
        # got_user_options = UserOptions(mock_args)

        # self.assertEqual(
        #     got_user_options.src_folder,
        #     Path("src/"),
        #     f"expected 'src/' but got {got_user_options.src_folder}",
        # )
        # self.assertEqual(
        #     got_user_options.dst_folder,
        #     Path("dst/"),
        #     f"expected 'dst/' but got {got_user_options.dst_folder}",
        # )
        # self.assertEqual(
        #     got_user_options.used_folder,
        #     Path("used/"),
        #     f"expected 'used/' but got {got_user_options.used_folder}",
        # )
        # self.assertEqual(
        #     got_user_options.num_files, 5, f"expected 5 but got {got_user_options.num_files}"
        # )
        # self.assertListEqual(
        #     got_user_options.glob_filters,
        #     ["glob.*"],
        #     f"expected ['glob.*'] but got {got_user_options.glob_filters}",
        # )

    # def test_user_options_constructor_optional(self):
    #     """Checks that the arguments have the expected values when not passing the optional args"""
    #     MockArgs = namedtuple("MockArgs", ["src", "dst", "used", "num_files", "glob"])
    #     mock_args = MockArgs(src="src/", dst="dst/", used=None, num_files=5, glob=["glob.*"])
    #     got_user_options = UserOptions(mock_args)

    #     self.assertEqual(
    #         got_user_options.src_folder,
    #         Path("src/"),
    #         f"expected 'src/' but got {got_user_options.src_folder}",
    #     )
    #     self.assertEqual(
    #         got_user_options.dst_folder,
    #         Path("dst/"),
    #         f"expected 'dst/' but got {got_user_options.dst_folder}",
    #     )
    #     self.assertEqual(
    #         got_user_options.used_folder,
    #         Path("src/seen/"),
    #         f"expected 'seen/' but got {got_user_options.used_folder}",
    #     )
    #     self.assertEqual(
    #         got_user_options.num_files, 5, f"expected 5 but got {got_user_options.num_files}"
    #     )
    #     self.assertListEqual(
    #         got_user_options.glob_filters,
    #         ["glob.*"],
    #         f"expected ['glob.*'] but got {got_user_options.glob_filters}",
    #     )

    # @patch.object(Path, "exists", return_value=True)
    # def test_user_options_validate_happy_path(self, mock_exists):
    #     """Checks happy path for UserOptions.validate() by way of mocking Path.exists()
    #     making it to return True no matter what
    #     """
    #     TestArgs = namedtuple("TestArgs", ["src", "dst", "used", "num_files", "glob"])
    #     test_args = TestArgs(src="src/", dst="dst/", used=None, num_files=5, glob=["glob.*"])
    #     test_user_options = UserOptions(test_args)
    #     try:
    #         test_user_options.validate()
    #     except Exception as ex:  # pylint: disable=broad-exception-caught
    #         self.fail(f"No exception expected but {type(ex)}: {ex} was raised")
    #     else:
    #         self.assertEqual(
    #             mock_exists.call_count,
    #             3,
    #             f"expected exists to be called 3 times, but was called {mock_exists.call_count}",
    #         )

    # def test_user_options_validate_unhappy_path_src(self):
    #     """Checks unhappy path for UserOptions.validate() by way of mocking the folder.exists"""

    #     TestArgs = namedtuple("TestArgs", ["src", "dst", "used", "num_files", "glob"])
    #     TestCaseData = namedtuple(
    #         "TestCaseData",
    #         ["args", "src_exists", "dst_exists", "used_exists", "expected_exception"],
    #     )
    #     test_cases = {
    #         "src folder not exists": TestCaseData(
    #             args=TestArgs(src="src/", dst="dst/", used=None, num_files=5, glob=["glob.*"]),
    #             src_exists=False,
    #             dst_exists=True,
    #             used_exists=True,
    #             expected_exception=RandFilePickError,
    #         ),
    #         "dst folder not exists": TestCaseData(
    #             args=TestArgs(src="src/", dst="dst/", used=None, num_files=5, glob=["glob.*"]),
    #             src_exists=True,
    #             dst_exists=False,
    #             used_exists=True,
    #             expected_exception=RandFilePickError,
    #         ),
    #         "used folder not exists": TestCaseData(
    #             args=TestArgs(src="src/", dst="dst/", used=None, num_files=5, glob=["glob.*"]),
    #             src_exists=True,
    #             dst_exists=True,
    #             used_exists=False,
    #             expected_exception=RandFilePickError,
    #         ),
    #         "folders exists but negative num files": TestCaseData(
    #             args=TestArgs(num_files=-1, src="src/", dst="dst/", used=None, glob=["glob.*"]),
    #             src_exists=True,
    #             dst_exists=True,
    #             used_exists=True,
    #             expected_exception=ValueError,
    #         ),
    #         "folders exists but zero num files": TestCaseData(
    #             args=TestArgs(num_files=0, src="src/", dst="dst/", used=None, glob=["glob.*"]),
    #             src_exists=True,
    #             dst_exists=True,
    #             used_exists=True,
    #             expected_exception=ValueError,
    #         ),
    #     }

    #     for test_title, test_data in test_cases.items():
    #         test_args = TestArgs(*test_data.args)
    #         test_user_options = UserOptions(test_args)
    #         test_user_options.src_folder = Mock(name="src_folder_mock")
    #         test_user_options.src_folder.exists.return_value = test_data.src_exists
    #         test_user_options.dst_folder = Mock(name="dst_folder_mock")
    #         test_user_options.dst_folder.exists.return_value = test_data.dst_exists
    #         test_user_options.used_folder = Mock(name="used_folder_mock")
    #         test_user_options.used_folder.exists.return_value = test_data.used_exists

    #         with self.assertRaises(
    #             test_data.expected_exception,
    #             msg=f"{test_title}: expected {type(test_title)} but something different happened",
    #         ):
    #             test_user_options.validate()

    # def test_user_options_str(self):
    #     """Tests UserOptions.__str__ method (for completion)"""
    #     MockArgs = namedtuple("MockArgs", ["src", "dst", "used", "num_files", "glob"])
    #     mock_args = MockArgs(src="src/", dst="dst/", used="used/", num_files=5, glob=["glob.*"])
    #     got_user_options = UserOptions(mock_args)
    #     got_user_options_str = str(got_user_options)
    #     expected_user_options = "src=src, patterns=['glob.*'], used=used, dst=dst, num_files=5"
    #     self.assertEqual(
    #         got_user_options_str,
    #         expected_user_options,
    #         f"expected {expected_user_options} but got {got_user_options_str}",
    #     )

    # def test_user_options_repr(self):
    #     """Tests UserOptions.__repr__ method (for completion)"""
    #     MockArgs = namedtuple("MockArgs", ["src", "dst", "used", "num_files", "glob"])
    #     mock_args = MockArgs(src="src/", dst="dst/", used="used/", num_files=5, glob=["glob.*"])
    #     got_user_options = UserOptions(mock_args)
    #     got_user_options_str = repr(got_user_options)
    #     expected_user_options = "UserOptions(src_folder=src, dst_folder=dst, glob_filters=['glob.*'], used_folder=used, num_files=5)" # python: disable=line-too-long
    #     self.assertEqual(
    #         got_user_options_str,
    #         expected_user_options,
    #         f"expected {expected_user_options} but got {got_user_options_str}",
    #     )


if __name__ == "__main__":
    unittest.main()
