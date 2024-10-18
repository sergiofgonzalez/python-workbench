"""
wc - A Python implementation of a subset of Unix/Linux wc command capabilities
"""

import fileinput
import sys
from argparse import ArgumentParser

USAGE = """Usage: wc [OPTION]... [FILE]...
(A Python implementation of a subset of wc command capabilities)

Print newline, word, and byte counts for each FILE, and a total line if
more than one FILE is specified.  A word is a non-zero-length sequence of
characters delimited by white space.

With no FILE, or when FILE is -, read standard input.

The options below may be used to select which counts are printed, always in
the following order: newline, word, character, byte, maximum line length.
  -c, --bytes            print the byte counts
  -l, --lines            print the newline counts
  -w, --words            print the word counts
      --help     display this help and exit
"""

STDIN_FILENAME = "-"


def get_counts_for_file(filename: str) -> tuple:
    """
    Gets the lines, words, and bytes counts for the given filename

    Args:
        filename: the name of the file to scan

    Returns:
        a tuple with the filename, lines, words, and bytes count (in that order)
    """
    num_lines = 0
    num_words = 0
    num_bytes = 0
    try:
        for line in fileinput.input(filename):
            num_lines += 1
            num_words += len(line.split())
            num_bytes += len(line)
        return filename, num_lines, num_words, num_bytes
    except FileNotFoundError as e:
        print(f"wc: {filename}: {e.strerror}")
        sys.exit(1)
    except PermissionError as e:
        print(f"wc: {filename}: {e.strerror}")
        sys.exit(1)
    except Exception as e:  # pylint: W0718:disable=broad-exception-caught
        print(f"wc: {filename}: {e}")


def print_counts_report(
    counts: list,
    count_lines: bool | None,
    count_words: bool | None,
    count_bytes: bool | None,
) -> None:
    if count_lines is None and count_words is None and count_bytes is None:
        count_lines = True
        count_words = True
        count_bytes = True

    total_num_lines = 0
    total_num_words = 0
    total_num_bytes = 0
    for filename, num_lines, num_words, num_bytes in counts:
        total_num_lines += num_lines
        total_num_words += num_words
        total_num_bytes += num_bytes
        if count_lines:
            print(num_lines, end=" ")
        if count_words:
            print(num_words, end=" ")
        if count_bytes:
            print(num_bytes, end=" ")
        if filename != STDIN_FILENAME:
            print(filename)
        else:
            print()

    if len(counts) > 1:
        if count_lines:
            print(total_num_lines, end=" ")
        if count_words:
            print(total_num_words, end=" ")
        if count_bytes:
            print(total_num_bytes, end=" ")
        print("total")


def main():
    """Controlling function for wc program"""
    parser = ArgumentParser(usage=USAGE)

    # required arg: must be zero or more
    parser.add_argument("filenames", nargs="*", help="files to scan")

    # options
    parser.add_argument(
        "-c",
        "--bytes",
        dest="count_bytes",
        action="store_true",
        default=None,
        help="print the byte counts",
    )

    parser.add_argument(
        "-l",
        "--lines",
        dest="count_lines",
        action="store_true",
        default=None,
        help="print the newline counts",
    )
    parser.add_argument(
        "-w",
        "--words",
        dest="count_words",
        action="store_true",
        default=None,
        help="print the word counts",
    )

    args = parser.parse_args()
    counts = []
    if len(args.filenames) == 0:
        counts.append(get_counts_for_file(STDIN_FILENAME))
    else:
        for filename in args.filenames:
            counts.append(get_counts_for_file(filename))
    print_counts_report(
        counts, args.count_lines, args.count_words, args.count_bytes
    )


if __name__ == "__main__":
    main()
