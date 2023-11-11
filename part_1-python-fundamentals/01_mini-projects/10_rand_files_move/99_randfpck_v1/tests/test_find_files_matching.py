"""find_files_matching function tests"""
import re
import unittest
from collections import namedtuple
from pathlib import Path
from unittest.mock import call, patch

from randfpck.main import find_files_matching


class TestFindFilesMatching(unittest.TestCase):
    """Test the find_files_matching function features"""

    def test_find_files_matching_unhappy_path(self):
        """Tests the find_files_matching function unhappy path"""

        TestCase = namedtuple("TestCase", ["folder", "patterns"])

        test_cases = {
            "empty folder and patterns": TestCase(folder=None, patterns=None),
            "empty folder only": TestCase(folder=None, patterns=["*"]),
            "empty patterns only": TestCase(folder=Path("f"), patterns=None),
            "empty list": TestCase(folder=Path("f"), patterns=[]),
        }

        for test_case, test_data in test_cases.items():
            with self.assertRaises(
                ValueError,
                msg=f"{test_case}: expected ValueError was not raised",
            ):
                find_files_matching(
                    folder=test_data.folder, patterns=test_data.patterns
                )

    def test_find_files_matching(self):
        """Tests the find_files_matching function by way of mocking the glob
        library
        """

        def get_tailored_side_effect(expected_files):
            """Returns a a function that can be plugged into the side_effects of
            a mock glob to get the list of files.
            This is overly complicated and maybe unnecessary, but has been left
            here for reference.
            """

            def glob_side_effects(
                pattern: str, root_dir
            ):  # pylint: disable=unused-argument
                updated_pattern = pattern.replace(".", r"\.")
                updated_pattern = updated_pattern.replace("*", r".+")

                re_pattern = re.compile(updated_pattern)
                result_files = []
                for file in expected_files:
                    if re_pattern.match(file):
                        result_files.append(file)
                return result_files

            return glob_side_effects

        TestCase = namedtuple(
            "TestCase", ["folder", "patterns", "expected_files"]
        )
        test_cases = {
            "multiple patterns, multiple files": TestCase(
                folder="path/to/folder",
                patterns=["*.txt", "*.md"],
                expected_files=[
                    "file1.txt",
                    "file2.txt",
                    "file1.md",
                    "file2.md",
                ],
            ),
            "single pattern, multiple file": TestCase(
                folder="path/to/folder",
                patterns=["*.txt"],
                expected_files=[
                    "file1.txt",
                    "file2.txt",
                ],
            ),
            "single pattern, one file": TestCase(
                folder="path/to/folder",
                patterns=["*.txt"],
                expected_files=[
                    "file.txt",
                ],
            ),
            "multiple patterns, empty dir": TestCase(
                folder="path/to/folder",
                patterns=["*.txt", "*.md"],
                expected_files=[],
            ),
            "single pattern, empty dir": TestCase(
                folder="path/to/folder",
                patterns=["*"],
                expected_files=[],
            ),
        }

        for test_case, test_data in test_cases.items():
            with patch("randfpck.main.glob") as mock_glob:
                mock_glob.glob.side_effect = get_tailored_side_effect(
                    test_data.expected_files
                )
                got_files = find_files_matching(
                    folder=Path(test_data.folder), patterns=test_data.patterns
                )
                self.assertListEqual(
                    got_files,
                    test_data.expected_files,
                    f"{test_case}: expected {test_data.expected_files} "
                    f"but got {got_files}",
                )

                # This is going a bit beyond what should be tested, but keeping
                # it for reference.
                # Reason being: I'm actually checking how the function is being
                # implemented, which I shouldn't do.
                self.assertEqual(
                    mock_glob.glob.call_count,
                    len(test_data.patterns),
                    (
                        f"{test_case}: expected glob.glob "
                        f"to be called {len(test_data.patterns)} times "
                        f"but was called {mock_glob.glob.call_count} times"
                    ),
                )
                mock_glob.glob.assert_has_calls(
                    [
                        call(pattern, root_dir=Path(test_data.folder))
                        for pattern in test_data.patterns
                    ]
                )
