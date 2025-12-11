"""Test cases for mathutils module."""

import pytest

from utils.mathutils import add


def test_add_ints() -> None:
    """Test addition of two integers."""
    assert add(2, 3) == 5  # noqa: PLR2004


def test_add_floats() -> None:
    """Test addition of two floats."""
    assert add(2.5, 3.5) == 6.0  # noqa: PLR2004


def test_add_mixed() -> None:
    """Test addition of an integer and a float."""
    assert add(2, 3.5) == 5.5  # noqa: PLR2004


def test_add_strings() -> None:
    """Test addition of two strings."""
    with pytest.raises(TypeError):
        add("Hello, ", "World!")  # type: ignore  # noqa: PGH003


def test_add_string_and_number() -> None:
    """Test addition of a string and a number."""
    with pytest.raises(TypeError):
        add("Hello, ", 5)  # type: ignore  # noqa: PGH003


def test_add_none() -> None:
    """Test addition of None and a number."""
    with pytest.raises(TypeError):
        add(None, 5)  # type: ignore  # noqa: PGH003
