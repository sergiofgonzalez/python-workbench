import unittest
from unittest.mock import patch, MagicMock
from someclass import SomeClass



class TestMockedPaths(unittest.TestCase):


    def test_do_something_with_files(self):
        """First approach for mocking SomeClass.do_something_with_files"""

        with (
            # We patch the class ctor only
            patch.object(SomeClass, "__init__", return_value=None),
            # We patch the pathlib.Path as used in someclass.py module
            patch("someclass.Path", autospec=True) as mocked_path
        ):
            # Invoking the class ctor (note: only the ctor was mock, not the other methods)
            mock_some_class = SomeClass("something")

            # Setting mock values for the attributes
            mock_some_class.folder_path = "path/to/file"
            mock_some_class.files = ["mock_file1"]

            # Setting the mock for file operations:
            # At the beginning of the class we have a:
            #  file_path = Path(self.folder_path) / file
            # to mock the subsequent is_dir call we need to do some complex mocking
            # which I don't know it's really useful from the testing perspective,
            # as it assumes deep knowledge of the implementation:
            # For example, if instead of doing Path(self.folder_path) / file
            # we do Path(self.folder_path + "/" + file) then the mock wouldn't work
            # this screams for a refactoring of the function
            mocked_path.return_value.__truediv__.return_value.is_dir.return_value = False
            mocked_path.return_value.__truediv__.return_value.is_symlink.return_value = False

            # Invoke the method under test with the mock values
            mock_some_class.do_something_with_files()


    def test_do_something_with_files_2(self):
        """Trying to approach mocking of SomeClass.do_something_with_files in a
        more maintainable way that doesn't require a deep understanding.
        """

        with (
            # We patch the class ctor only
            patch.object(SomeClass, "__init__", return_value=None)
        ):
            # Invoking the class ctor (note: only the ctor was mock, not the other methods)
            mock_some_class = SomeClass("something")

            # Setting mock values for the attributes
            mock_some_class.folder_path = "path/to/file"
            mock_some_class.files = [MagicMock(name="mock file 1")]
            mock_some_class.files[0].is_dir.return_value = True
            mock_some_class.files[0].is_symlink.return_value = False

            # Invoke the method under test with the mock values
            mock_some_class.do_something_with_files()


if __name__ == "__main__":
    unittest.main()