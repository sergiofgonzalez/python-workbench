"""Shared and fixtures with scope other than function."""

import pytest

@pytest.fixture(scope="module")
def module_fixture():
    print("==> This is executed before each test file")
    yield
    print("==> This is executed after each test file")