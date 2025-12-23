"""pytest unit tests 'utils/reporting.py' module."""

from unittest.mock import MagicMock

from utils.reporting import (
    print_full_report,
    print_summary_report,
)


def test_print_summary_report(capfd: MagicMock) -> None:
    """Test print_summary_report function."""
    word_count = {
        "apple": 4,
        "banana": 2,
        "cherry": 5,
        "date": 1,
        "elderberry": 3,
    }
    expected_most_common = [
        "'cherry' occurs 5 times.",
        "'apple' occurs 4 times.",
        "'elderberry' occurs 3 times.",
    ]
    expected_least_common = [
        "'date' occurs 1 time.",
        "'banana' occurs 2 times.",
        "'elderberry' occurs 3 times.",
    ]

    print_summary_report(word_count, num_words=3)
    captured = capfd.readouterr()
    output_lines = captured.out.strip().splitlines()

    for expected_line in expected_most_common + expected_least_common:
        assert expected_line in output_lines


def test_print_full_report(capfd: MagicMock) -> None:
    """Test print_full_report function."""
    word_count = {
        "apple": 2,
        "banana": 1,
        "cherry": 3,
    }
    expected_outputs = [
        "'apple' occurs 2 times.",
        "'banana' occurs 1 time.",
        "'cherry' occurs 3 times.",
    ]

    print_full_report(word_count)
    captured = capfd.readouterr()
    output_lines = captured.out.strip().splitlines()

    for expected_line in expected_outputs:
        assert expected_line in output_lines
