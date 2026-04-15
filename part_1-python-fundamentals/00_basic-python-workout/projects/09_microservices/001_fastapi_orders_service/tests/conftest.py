"""Shared fixtures for the test suite."""

from collections.abc import Iterator

import pytest

from app.api.orders import fake_orders_db


@pytest.fixture(autouse=True)
def _clear_orders_db() -> Iterator[None]:
    """Clear the in-memory orders database between tests."""
    yield
    fake_orders_db.clear()
