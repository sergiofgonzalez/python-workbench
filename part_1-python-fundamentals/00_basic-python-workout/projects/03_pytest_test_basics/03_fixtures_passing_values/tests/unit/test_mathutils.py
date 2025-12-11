"""Test cases for mathutils module."""

from collections.abc import Generator

import pytest

from utils.mathutils import add


@pytest.fixture
def happy_path_test_data() -> Generator[dict[str, dict[str, float]], None, None]:
    """Setup and teardown for tests."""
    test_scenarios = {
        "add_ints": {"num1": 2, "num2": 3, "expected": 5},
        "add_floats": {"num1": 2.5, "num2": 3.5, "expected": 6.0},
        "add_mixed": {"num1": 2, "num2": 3.5, "expected": 5.5},
    }
    yield test_scenarios
    # Teardown code can be added here if needed
    print("Tearing down tests...")


@pytest.fixture
def negative_scenarios_test_data() -> dict[str, dict[str, float | str | TypeError]]:
    """Setup and teardown for tests."""
    test_scenarios = {
        "add_strings": {"num1": "foo", "num2": "bar", "expected": TypeError},
        "add_str_num": {"num1": "foo", "num2": 5, "expected": TypeError},
        "add_num_str": {"num1": 5, "num2": "foo", "expected": TypeError},
        "add_none_num": {"num1": None, "num2": 5, "expected": TypeError},
        "add_num_none": {"num1": 5, "num2": None, "expected": TypeError},
    }
    # You can also return instead of yield if no teardown is needed
    return test_scenarios  # noqa: RET504


def test_add_happy_path(happy_path_test_data: dict[str, dict[str, float]]) -> None:
    """Test happy path scenarios."""
    for scenario, data in happy_path_test_data.items():
        actual = add(data["num1"], data["num2"])
        assert actual == data["expected"], f"Failed in scenario: {scenario}"


def test_add_negative_scenarios(
    negative_scenarios_test_data: dict[str, dict[str, float | str | TypeError]],
) -> None:
    """Test negative scenarios."""
    for data in negative_scenarios_test_data.values():
        with pytest.raises(data["expected"]):  # type: ignore[union-attr]
            add(data["num1"], data["num2"])  # type: ignore  # noqa: PGH003
