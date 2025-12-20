"""pytest unit tests for creature.py."""

from pathlib import Path
from unittest.mock import MagicMock, mock_open, patch

from main_v1 import (
    get_top_n_least_common_words,
    get_top_n_most_common_words,
    get_word_count,
    normalize_text_file,
    normalize_text_line,
    print_full_report,
    print_summary_report,
    print_word_count,
)


def test_normalize_text_file() -> None:
    """Test normalize_text_file function using mocks for file reading and writing."""
    sample_input = "Hello, World!\nThis is a test.\n"
    expected_output = ["hello\n", "world\n", "this\n", "is\n", "a\n", "test\n"]
    mock_in_file = mock_open(read_data=sample_input)
    mock_out_file = mock_open()

    def open_side_effect(mode: str, *args: object, **kwargs: object) -> MagicMock:  # noqa: ARG001
        """Return different mock based on file open mode."""
        if mode == "r":
            return mock_in_file()
        return mock_out_file()

    with patch.object(Path, "open", side_effect=open_side_effect):
        normalize_text_file(Path("dummy_input.txt"), Path("dummy_output.txt"))

    # Retrieve the written data from the mock output file
    written_data = []
    handle = mock_out_file()
    handle.write.assert_called()  # Ensure write was called
    for call in handle.write.call_args_list:
        written_data.append(call.args[0])  # noqa: PERF401

    assert written_data == expected_output


def test_normalize_text_line() -> None:
    """Test the normalize_text_line function."""
    test_cases = [
        ("Hello, World!", ["hello", "world"]),
        ("  Leading and trailing spaces  ", ["leading", "and", "trailing", "spaces"]),
        (
            "Punctuation! Should; be: removed.",
            ["punctuation", "should", "be", "removed"],
        ),
        ("Mixed CASE Words", ["mixed", "case", "words"]),
        ("Numbers 123 and symbols #@$%", ["numbers", "123", "and", "symbols"]),
        ("", []),
        ("   ", []),
    ]

    for input_line, expected_output in test_cases:
        assert normalize_text_line(input_line) == expected_output


@patch.object(Path, "open")
def test_get_word_count(mock_path_open: MagicMock) -> None:
    """Test the get_word_count function using mocks for file reading."""
    sample_text = "apple\nbanana\napple\ncherry\nbanana\ndate\nelderberry\napple\n"
    expected_word_count = {
        "apple": 3,
        "banana": 2,
        "cherry": 1,
        "date": 1,
        "elderberry": 1,
    }
    mock_path_open.side_effect = mock_open(read_data=sample_text)
    word_count = get_word_count(Path("dummy_path.txt"))
    assert word_count == expected_word_count


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


def test_print_word_count(capfd: MagicMock) -> None:
    """Test print_word_count function."""
    test_cases = [
        ("apple", 1, "'apple' occurs 1 time."),
        ("banana", 2, "'banana' occurs 2 times."),
        ("cherry", 0, "'cherry' occurs 0 times."),
    ]

    for word, count, expected_output in test_cases:
        print_word_count(word, count)
        captured = capfd.readouterr()
        assert captured.out.strip() == expected_output


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


def test_get_top_n_most_common_words() -> None:
    """Test the get_top_n_most_common_words function."""
    word_count = {
        "apple": 4,
        "banana": 2,
        "cherry": 5,
        "date": 1,
        "elderberry": 3,
    }
    expected_top_3 = [("cherry", 5), ("apple", 4), ("elderberry", 3)]
    assert get_top_n_most_common_words(word_count, 3) == expected_top_3


def test_get_top_n_least_common_words() -> None:
    """Test the get_top_n_least_common_words function."""
    word_count = {
        "apple": 4,
        "banana": 2,
        "cherry": 5,
        "date": 1,
        "elderberry": 3,
    }
    expected_least_3 = [("date", 1), ("banana", 2), ("elderberry", 3)]
    assert get_top_n_least_common_words(word_count, 3) == expected_least_3


def test_word_count() -> None:
    """Test word count functionality."""
    sample_text = "Apple banana apple. Cherry! Banana? Date, elderberry apple."
    expected_word_count = {
        "apple": 3,
        "banana": 2,
        "cherry": 1,
        "date": 1,
        "elderberry": 1,
    }

    # Simulate reading lines from a file
    lines = sample_text.splitlines()
    word_count: dict[str, int] = {}
    for line in lines:
        words = normalize_text_line(line)
        for word in words:
            word_count[word] = word_count.get(word, 0) + 1

    assert word_count == expected_word_count
