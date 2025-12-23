"""pytest unit tests 'utils/normalize.py' module."""

from pathlib import Path
from unittest.mock import MagicMock, mock_open, patch

from utils.normalize import (
    normalize_text_file,
    normalize_text_line,
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
