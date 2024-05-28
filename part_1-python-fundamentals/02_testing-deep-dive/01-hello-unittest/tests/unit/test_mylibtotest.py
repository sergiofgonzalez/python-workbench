"""Testing mylibtotest.py"""

import unittest

from prgtotest.mylibtotest import add


class TestAddFunction(unittest.TestCase):

    def setUp(self) -> None:
        # This method is called before each test
        ...

    def tearDown(self) -> None:
        # This method is called after each test
        ...

    def test_add_integers(self) -> None:
        """Test adding two integers"""
        result = add(1, 2)
        expected = 3
        self.assertEqual(result, expected)

    def test_add_floats(self) -> None:
        """Test adding two floats"""
        result = add(1.1, 2.2)
        expected = 3.3
        self.assertAlmostEqual(result, expected)

    def test_add_mixed(self) -> None:
        """Test adding an integer and a float"""
        result = add(1, 2.2)
        expected = 3.2
        self.assertAlmostEqual(result, expected)

    def test_add_number_and_string(self) -> None:
        """Test adding a number and a string"""
        with self.assertRaises(TypeError):
            add(1, "2") # type: ignore


if __name__ == "__main__":
    unittest.main()
