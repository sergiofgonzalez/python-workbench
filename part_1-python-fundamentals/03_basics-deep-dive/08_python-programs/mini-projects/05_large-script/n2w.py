#! /usr/bin/env python3
"""
n2w: number to words conversion module: contains function `num_2_words()` and
can also be run as a script.
usage as a script: `n2w <number>`
Converts a number to its English word representation.
The number must be a whole integer from 0 to 999,999,999,999,999 (commas are
optional)
example:
n2w 10003103
ten million three thousand one hundred three

"""
import argparse
import string
import sys

_1_to_9_dict = {
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

_10_to_19_dict = {
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

_20_to_90_dict = {
    "2": "twenty",
    "3": "thirty",
    "4": "forty",
    "5": "fifty",
    "6": "sixty",
    "7": "seventy",
    "8": "eighty",
    "9": "ninety",
}

_magnitude_list = [
    (0, ""),
    (3, "thousand"),
    (6, "million"),
    (9, "billion"),
    (12, "trillion"),
    (15, ""),
]


def num_2_words(num_str: str) -> str:
    """
    Convert a number to its English word representation.

    Args:
        num_str: str: a string representing a number
    Returns:
        str: the English word representation of the number
    """
    if num_str == "0":
        return "zero"
    num_str = num_str.replace(",", "")
    num_len = len(num_str)
    max_digits = _magnitude_list[-1][0]
    if num_len > max_digits:
        return f"Can't handle numbers with more than {max_digits} digits"
    num_str = "00" + num_str
    word_string = ""
    for mag, name in _magnitude_list:
        if mag >= num_len:
            return word_string
        else:
            hundreds, tens, ones = (
                num_str[-mag - 3],
                num_str[-mag - 2],
                num_str[-mag - 1],
            )
            if not (hundreds == tens == ones == "0"):
                word_string = (
                    _handle_1_to_999(hundreds, tens, ones) + " " + name + " " + word_string
                )

def _handle_1_to_999(hundreds, tens, ones):
    if hundreds == "0":
        return _handle_1_to_99(tens, ones)
    else:
        return (
            _1_to_9_dict[hundreds] + " hundred " + _handle_1_to_99(tens, ones)
        )

def _handle_1_to_99(tens, ones):
    if tens == "0":
        return _1_to_9_dict[ones]
    if tens == "1":
        return _10_to_19_dict[ones]
    else:
        return _20_to_90_dict[tens] + " " + _1_to_9_dict[ones]

def test():
    values = sys.stdin.read().split()
    for val in values:
        print(f"{val} = {num_2_words(val)}")


def main():
    parser = argparse.ArgumentParser(usage=__doc__)
    parser.add_argument("number", nargs="*")
    parser.add_argument("-t", "--test", dest="test", action="store_true", default=False, help="Test mode: reads from stdin")
    args = parser.parse_args()
    if args.test:
        test()
    else:
        try:
            result = num_2_words(args.number[0])
        except KeyError:
            parser.error("argument contains non-digits")
        else:
            print(f"For {args.number[0]}, say: {result}")


if __name__ == "__main__":
    main()
else:
    print("using n2w as a module")
