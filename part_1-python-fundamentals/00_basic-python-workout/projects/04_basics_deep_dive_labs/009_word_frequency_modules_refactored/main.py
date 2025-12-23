"""Calculates word frequency from a text file."""

from pathlib import Path

from utils.counting import get_word_count
from utils.normalize import normalize_text_file
from utils.reporting import print_full_report, print_summary_report

in_file_path = Path("data/moby_01.txt")
out_file_path = Path("data/moby_01_normalized.txt")


def main() -> None:
    """Application entry point."""
    normalize_text_file(in_file_path, out_file_path)
    word_count = get_word_count(out_file_path)
    print_full_report(word_count)
    print_summary_report(word_count)


if __name__ == "__main__":
    main()
