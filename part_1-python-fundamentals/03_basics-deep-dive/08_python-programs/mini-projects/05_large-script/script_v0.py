"""
script - main script for a larger program tht returns the English-language
name for a given number between 0 an 99.
"""
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
    "9": "nine"
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
    "9": "nineteen"
}

_20_to_90_dict = {
    "2": "twenty",
    "3": "thirty",
    "4": "forty",
    "5": "fifty",
    "6": "sixty",
    "7": "seventy",
    "8": "eighty",
    "9": "ninety"
}

def num_2_words(num_str: str):
    if num_str == "0":
        return "zero"
    if len(num_str) > 2:
        return "Number must be between 0 and 99"
    num_str = "0" + num_str
    tens, ones = num_str[-2], num_str[-1]
    if tens == "0":
        return _1_to_9_dict[ones]
    if tens == "1":
        return _10_to_19_dict[ones]
    else:
        return _20_to_90_dict[tens] + " " + _1_to_9_dict[ones]

def main():
    print(num_2_words(sys.argv[1]))

if __name__ == "__main__":
    main()