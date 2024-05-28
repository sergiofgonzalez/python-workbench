"""Tests for the 'the_code_to_test' library"""

import pytest
import math
from my_package.the_code_to_test import add


@pytest.fixture(name="setup_and_tear_down")
def test_setup_and_teardown():
    print("This is executed before each test")
    yield
    print("This is executed after each test")


def test_add_integers(setup_and_tear_down):
    got = add(1, 2)
    expected = 3
    assert got == expected


def test_add_floats(setup_and_tear_down):
    got = add(1.1, 2.2)
    expected = 3.3
    assert math.isclose(got, expected, rel_tol=1e-9)


def test_add_strings(setup_and_tear_down):
    got = add("1", "2")
    expected = "12"
    assert got == expected


def test_add_mixed_types(setup_and_tear_down):
    with pytest.raises(TypeError):
        add(1, "2")
