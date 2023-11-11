"""Testing UserOptions class"""
import unittest
from collections import namedtuple
from unittest.mock import Mock, patch

from randfpck.main import Path, RandFilePickError, UserOptions


class TestUserOptions(unittest.TestCase):
    """Test the UserOptions class features"""

    def test_user_options_constructor(self):
        """Checks that the arguments have the expected values when passing all
        args.
        """
        MockArgs = namedtuple(
            "MockArgs", ["src", "dst", "used", "num_files", "glob"]
        )
        mock_args = MockArgs(
            src="src/", dst="dst/", used="used/", num_files=5, glob=["glob.*"]
        )
        got_user_options = UserOptions(mock_args)

        self.assertEqual(
            got_user_options.src_folder,
            Path("src/"),
            f"expected 'src/' but got {got_user_options.src_folder}",
        )
        self.assertEqual(
            got_user_options.dst_folder,
            Path("dst/"),
            f"expected 'dst/' but got {got_user_options.dst_folder}",
        )
        self.assertEqual(
            got_user_options.used_folder,
            Path("used/"),
            f"expected 'used/' but got {got_user_options.used_folder}",
        )
        self.assertEqual(
            got_user_options.num_files,
            5,
            f"expected 5 but got {got_user_options.num_files}",
        )
        self.assertListEqual(
            got_user_options.glob_filters,
            ["glob.*"],
            f"expected ['glob.*'] but got {got_user_options.glob_filters}",
        )

    def test_user_options_constructor_optional(self):
        """Checks that the arguments have the expected values when not passing
        the optional args.
        """
        MockArgs = namedtuple(
            "MockArgs", ["src", "dst", "used", "num_files", "glob"]
        )
        mock_args = MockArgs(
            src="src/", dst="dst/", used=None, num_files=5, glob=["glob.*"]
        )
        got_user_options = UserOptions(mock_args)

        self.assertEqual(
            got_user_options.src_folder,
            Path("src/"),
            f"expected 'src/' but got {got_user_options.src_folder}",
        )
        self.assertEqual(
            got_user_options.dst_folder,
            Path("dst/"),
            f"expected 'dst/' but got {got_user_options.dst_folder}",
        )
        self.assertEqual(
            got_user_options.used_folder,
            Path("src/seen/"),
            f"expected 'seen/' but got {got_user_options.used_folder}",
        )
        self.assertEqual(
            got_user_options.num_files,
            5,
            f"expected 5 but got {got_user_options.num_files}",
        )
        self.assertListEqual(
            got_user_options.glob_filters,
            ["glob.*"],
            f"expected ['glob.*'] but got {got_user_options.glob_filters}",
        )

    @patch.object(Path, "exists", return_value=True)
    def test_user_options_validate_happy_path(self, mock_exists):
        """Checks happy path for UserOptions.validate() by way of mocking
        Path.exists() making it to return True no matter what.
        """
        TestArgs = namedtuple(
            "TestArgs", ["src", "dst", "used", "num_files", "glob"]
        )
        test_args = TestArgs(
            src="src/", dst="dst/", used=None, num_files=5, glob=["glob.*"]
        )
        test_user_options = UserOptions(test_args)
        try:
            test_user_options.validate()
        except Exception as ex:  # pylint: disable=broad-exception-caught
            self.fail(f"No exception expected but {type(ex)}: {ex} was raised")
        else:
            self.assertEqual(
                mock_exists.call_count,
                3,
                (
                    f"expected exists to be called 3 times, "
                    f"but was called {mock_exists.call_count}"
                ),
            )

    def test_user_options_validate_unhappy_path_src(self):
        """Checks unhappy path for UserOptions.validate() by way of mocking the
        folder.exists.
        """

        TestArgs = namedtuple(
            "TestArgs", ["src", "dst", "used", "num_files", "glob"]
        )
        TestCaseData = namedtuple(
            "TestCaseData",
            [
                "args",
                "src_exists",
                "dst_exists",
                "used_exists",
                "expected_exception",
            ],
        )
        test_cases = {
            "src folder not exists": TestCaseData(
                args=TestArgs(
                    src="src/",
                    dst="dst/",
                    used=None,
                    num_files=5,
                    glob=["glob.*"],
                ),
                src_exists=False,
                dst_exists=True,
                used_exists=True,
                expected_exception=RandFilePickError,
            ),
            "dst folder not exists": TestCaseData(
                args=TestArgs(
                    src="src/",
                    dst="dst/",
                    used=None,
                    num_files=5,
                    glob=["glob.*"],
                ),
                src_exists=True,
                dst_exists=False,
                used_exists=True,
                expected_exception=RandFilePickError,
            ),
            "used folder not exists": TestCaseData(
                args=TestArgs(
                    src="src/",
                    dst="dst/",
                    used=None,
                    num_files=5,
                    glob=["glob.*"],
                ),
                src_exists=True,
                dst_exists=True,
                used_exists=False,
                expected_exception=RandFilePickError,
            ),
            "folders exists but negative num files": TestCaseData(
                args=TestArgs(
                    num_files=-1,
                    src="src/",
                    dst="dst/",
                    used=None,
                    glob=["glob.*"],
                ),
                src_exists=True,
                dst_exists=True,
                used_exists=True,
                expected_exception=ValueError,
            ),
            "folders exists but zero num files": TestCaseData(
                args=TestArgs(
                    num_files=0,
                    src="src/",
                    dst="dst/",
                    used=None,
                    glob=["glob.*"],
                ),
                src_exists=True,
                dst_exists=True,
                used_exists=True,
                expected_exception=ValueError,
            ),
        }

        for test_title, test_data in test_cases.items():
            test_args = TestArgs(*test_data.args)
            test_user_options = UserOptions(test_args)
            test_user_options.src_folder = Mock(name="src_folder_mock")
            test_user_options.src_folder.exists.return_value = (
                test_data.src_exists
            )
            test_user_options.dst_folder = Mock(name="dst_folder_mock")
            test_user_options.dst_folder.exists.return_value = (
                test_data.dst_exists
            )
            test_user_options.used_folder = Mock(name="used_folder_mock")
            test_user_options.used_folder.exists.return_value = (
                test_data.used_exists
            )

            with self.assertRaises(
                test_data.expected_exception,
                msg=(
                    f"{test_title}: expected {type(test_title)} "
                    f"but something different happened"
                ),
            ):
                test_user_options.validate()

    def test_user_options_str(self):
        """Tests UserOptions.__str__ method (for completion)"""
        MockArgs = namedtuple(
            "MockArgs", ["src", "dst", "used", "num_files", "glob"]
        )
        mock_args = MockArgs(
            src="src/", dst="dst/", used="used/", num_files=5, glob=["glob.*"]
        )
        got_user_options = UserOptions(mock_args)
        got_user_options_str = str(got_user_options)
        expected_user_options = (
            "src=src, patterns=['glob.*'], used=used, dst=dst, num_files=5"
        )
        self.assertEqual(
            got_user_options_str,
            expected_user_options,
            f"expected {expected_user_options} but got {got_user_options_str}",
        )

    def test_user_options_repr(self):
        """Tests UserOptions.__repr__ method (for completion)"""
        MockArgs = namedtuple(
            "MockArgs", ["src", "dst", "used", "num_files", "glob"]
        )
        mock_args = MockArgs(
            src="src/", dst="dst/", used="used/", num_files=5, glob=["glob.*"]
        )
        got_user_options = UserOptions(mock_args)
        got_user_options_str = repr(got_user_options)
        expected_user_options = (
            "UserOptions(src_folder=src, dst_folder=dst, "
            "glob_filters=['glob.*'], used_folder=used, num_files=5)"
        )
        self.assertEqual(
            got_user_options_str,
            expected_user_options,
            f"expected {expected_user_options} but got {got_user_options_str}",
        )


if __name__ == "__main__":
    unittest.main(buffer=True)
