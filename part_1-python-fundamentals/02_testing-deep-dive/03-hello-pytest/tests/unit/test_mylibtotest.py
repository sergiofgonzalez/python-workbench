"""mylibttotest.py unit tests using PyTest framework"""

import pytest

from prgtotest.mylibtotest import add


@pytest.fixture(name="setup_teardown")
def test_setup_and_teardown():
    print("This is executed before each test")
    yield
    print("This is executed after each test")


def test_add_integers(setup_teardown): # pylint: disable=W0613:unused-argument
    actual = add(1, 2)
    expected = 3
    assert actual == expected


def test_add_floats(setup_teardown): # pylint: disable=W0613:unused-argument
    actual = add(1.1, 2.2)
    expected = 3.3
    assert actual == expected


def test_add_strings(setup_teardown): # pylint: disable=W0613:unused-argument
    actual = add("1", "2")
    expected = "12"
    assert actual == expected


def test_add_mixed_types(setup_teardown): # pylint: disable=W0613:unused-argument
    with pytest.raises(TypeError):
        add(1, "2")
