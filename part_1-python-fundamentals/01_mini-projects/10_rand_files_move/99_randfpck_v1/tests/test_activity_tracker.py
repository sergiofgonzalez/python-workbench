"""Testing ActivityTracker class"""
import unittest
from collections import namedtuple
from unittest.mock import MagicMock, patch

from randfpck.main import ActivityTracker, FolderFiles


class TestActivityTracker(unittest.TestCase):
    """Tests the ActivityTracker class features"""

    def test_ctor(self):
        """Tests the construction of the ActivityTracker class"""

        # no files in src folder
        with patch.object(FolderFiles, "__init__", return_value=None):
            mock_folder_files = FolderFiles(folder="path/to/folder")
            mock_folder_files.files = []

            got = ActivityTracker(5, mock_folder_files)
            self.assertEqual(got.num_files_to_pick, 5)
            self.assertEqual(got.files_picked, [])
            self.assertEqual(got.files_discarded, [])
            self.assertEqual(got.orig_src_folder_size, 0)

        # two files in src folder
        with patch.object(FolderFiles, "__init__", return_value=None):
            mock_folder_files = FolderFiles(folder="path/to/folder")
            mock_folder_files.files = ["file1.txt", "file2.txt"]

            got = ActivityTracker(1, mock_folder_files)
            self.assertEqual(got.num_files_to_pick, 1)
            self.assertEqual(got.files_picked, [])
            self.assertEqual(got.files_discarded, [])
            self.assertEqual(got.orig_src_folder_size, 2)

        # incorrect folder type parameters
        with self.assertRaises(
            TypeError, msg="expected TypeError but got something different"
        ):
            ActivityTracker(1, "path/to/folder")

    def test_process_done(self):
        Subtest = namedtuple(
            "Subtest",
            ["num_files_to_pick", "files", "files_picked", "expected"],
        )

        subtests = {
            "folder not empty, files picked": Subtest(
                num_files_to_pick=1,
                files=["file.txt"],
                files_picked=["file.txt"],
                expected=True,
            ),
            "folder empty, files picked": Subtest(
                num_files_to_pick=1,
                files=[],
                files_picked=["file.txt"],
                expected=True,
            ),
            "folder empty, files not picked": Subtest(
                num_files_to_pick=1, files=[], files_picked=[], expected=True
            ),
            "folder not empty, files not picked": Subtest(
                num_files_to_pick=2,
                files=["file.txt", "file.md"],
                files_picked=["file.txt"],
                expected=False,
            ),
        }

        for subtest_name, subtest_data in subtests.items():
            with (
                patch.object(ActivityTracker, "__init__", return_value=None),
            ):
                mock_activity_tracker = ActivityTracker(
                    subtest_data.num_files_to_pick, "path/to/folder"
                )
                mock_activity_tracker.num_files_to_pick = (
                    subtest_data.num_files_to_pick
                )
                mock_activity_tracker.src_folder_files = MagicMock()
                mock_activity_tracker.src_folder_files.files = (
                    subtest_data.files
                )
                mock_activity_tracker.files_picked = subtest_data.files_picked

                got = mock_activity_tracker.process_done()
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
