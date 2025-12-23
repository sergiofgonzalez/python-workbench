"""pytest unit tests 'utils/counting.py' module."""

from pathlib import Path
from unittest.mock import MagicMock, mock_open, patch

from utils.counting import (
    get_top_n_least_common_words,
    get_top_n_most_common_words,
    get_word_count,
)


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
