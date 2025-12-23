"""Configure pytest settings for unit tests."""

from collections.abc import Generator

import pytest


@pytest.fixture(scope="module")
def setup_and_teardown() -> Generator[None, None, None]:
    """Fixture to set up and tear down resources for tests."""
    # Setup code here
    print("\n>>> Setting up resources for tests... (should be executed once per module)")
    yield
    # Teardown code here
    print("\n>>> Tearing down resources for tests... (should be executed once per module)")