#!/usr/bin/env python3
"""n2w: number to words converter.

n2w.py: number to words conversion module: contains function `number_to_words()` and
can also be run as a script.

usage as a script: `n2w <number>`
Converts a number to its English word representation.
The number must be a whole integer from 0 to 999,999,999,999,999 (commas are
optional)

Example:
n2w 10003103
ten million three thousand one hundred three
"""

import argparse
import sys

_magnitudes = [
    (0, ""),
    (3, "thousand"),
    (6, "million"),
    (9, "billion"),
    (12, "trillion"),
    (15, "quadrillion"),
]

_handle_1_to_9_dict = {
    "0": "",
    "1": "one",
    "2": "two",
    "3": "three",
    "4": "four",
    "5": "five",
    "6": "six",
    "7": "seven",
    "8": "eight",
    "9": "nine",
}

_handle_10_to_19_dict = {
    "0": "ten",
    "1": "eleven",
    "2": "twelve",
    "3": "thirteen",
    "4": "fourteen",
    "5": "fifteen",
    "6": "sixteen",
    "7": "seventeen",
    "8": "eighteen",
    "9": "nineteen",
}

_handle_20_to_90_dict = {
    "2": "twenty",
    "3": "thirty",
    "4": "forty",
    "5": "fifty",
    "6": "sixty",
    "7": "seventy",
    "8": "eighty",
    "9": "ninety",
}


def _handle_1_to_999(hundreds: str, tens: str, ones: str) -> str:
    """Convert a three-digit number (given as separate digits) into words."""
    if hundreds == "0":
        return _handle_1_to_99(tens, ones)
    return _handle_1_to_9_dict[hundreds] + " hundred " + _handle_1_to_99(tens, ones)


def _handle_1_to_99(tens: str, ones: str) -> str:
    """Convert a two-digit number (given as separate digits) into words."""
    if tens == "0":
        return _handle_1_to_9_dict[ones]
    if tens == "1":
        return _handle_10_to_19_dict[ones]
    return _handle_20_to_90_dict[tens] + " " + _handle_1_to_9_dict[ones]


def number_to_words(num_str: str) -> str:
    """Convert a number into words."""
    if num_str == "0":
        return "zero"
    num_str = num_str.replace(",", "")
    num_len = len(num_str)
    max_digits = _magnitudes[-1][0]
    if num_len > max_digits:
        return f"Can't handle numbers with more than {max_digits} digits"
    if num_str.startswith("-"):
        return "Negative numbers are not supported"
    num_str = "00" + num_str  # Pad with leading zeros for easier grouping
    word_str = ""
    for magnitude, name in _magnitudes:
        if magnitude >= num_len:
            return word_str
        hundreds, tens, ones = (
            num_str[-(magnitude + 3)],
            num_str[-(magnitude + 2)],
            num_str[-(magnitude + 1)],
        )
        if not (hundreds == tens == ones == "0"):
            word_str = (
                _handle_1_to_999(hundreds, tens, ones) + " " + name + " " + word_str
            )
    return f"For some reasong word conversion failed: {word_str=}; num_str={num_str=}"


def test() -> None:
    """Run basic tests for number_to_words function."""
    values = sys.stdin.read().split()
    for value in values:
        print(f"{value} = {number_to_words(value)}")


def main() -> None:
    """Application entry point."""
    parser = argparse.ArgumentParser(
        usage=__doc__,
    )

    # Positional argument for the number to convert
    parser.add_argument(
        "number",
        nargs="*",  # One or more numbers
        help="The number to convert to words.",
    )

    # Optional
    parser.add_argument(
        "-t",
        "--test",
        dest="test_mode",
        action="store_true",
        default=False,
        help="Enable test mode: reads numbers from stdin instead of command line.",
    )

    # Parse the command-line arguments
    args = parser.parse_args()
    print(args)

    if args.test_mode:
        print("Test mode enabled. Reading numbers from stdin...")
        test()
    else:
        numbers = args.number
        for number in numbers:
            words = number_to_words(number)
            print(f"For {number}, say {words}")


if __name__ == "__main__":
    main()
