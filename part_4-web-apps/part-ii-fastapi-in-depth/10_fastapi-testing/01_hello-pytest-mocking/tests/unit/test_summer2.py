"""Second approach for testing the mod2.summer function using mocks"""
from unittest import mock
from hellomock import mod2


def test_summer_a():
    with mock.patch("hellomock.mod1.preamble", return_value=""):
        assert "3" == mod2.summer(1, 2)


# Alternatively, using a named mock
def test_summer_b():
    with mock.patch("hellomock.mod1.preamble") as mock_preamble:
        mock_preamble.return_value = ""
        assert "3" == mod2.summer(1, 2)

# Alternatively, using a decorator
@mock.patch("hellomock.mod1.preamble", return_value="")
def test_summer_c(mock_decorator_preamble):
    assert "3" == mod2.summer(1, 2)

# Alternatively, using a decorator and configuring the return value
@mock.patch("hellomock.mod1.preamble")
def test_summer_d(mock_decorator_preamble):
    mock_decorator_preamble.return_value = ""
    assert "3" == mod2.summer(1, 2)