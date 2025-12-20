# Basics deep-dive Labs
> a collection of labs on Python basics

## [001: basic statistics](001_basic_statistics/README.md)
> files, lists

Given a file with the monthly high temperature at Heathrow airport from 1948 to 2017 (data/in_data/380_basic_statistics/temp_heathrow.txt), read the file and find the following basic statistics without relying on any module:

1. Highest and lowest temperatures
1. Mean temperature (i.e., the average temperature)
1. Median temperature
1. Calculate the number of unique temperatures found in the file

## [002: normalizing a text file](002_text_file_normalization/README.md)
> files, strings, translation

In processing raw text, it's often necessary to clean and normalize the text before doing anything else.

For example, if you want to find the frequence of words in a text, it's quite common to normalize before calculating that frequency. It's also common to break the text into a series of words and write each one of them on its own line.

Read the first part of the first chapter of Moby Dick, normalizing it (making sure that everything is using either lowercase or uppercase), remove all punctuation, and write the words one per line to a second file.

## [003: Calculating the frequency of words in a text file](003_word_frequency_text_file/README.md)
> dictionaries, sorting, files, strings, translation

In processing raw text, it's often necessary to clean and normalize the text before doing anything else.

For example, if you want to find the frequence of words in a text, it's quite common to normalize before calculating that frequency. It's also common to break the text into a series of words and write each one of them on its own line.

Relying on the solution of [002: normalizing a text file](002_text_file_normalization/), read the first part of the first chapter of Moby Dick, normalizing it (making sure that everything is using either lowercase or uppercase), remove all punctuation, and write the words one per line to a second file.

While writing that file, implement the necessary logic to count the number of times each word occurs. That information will be used to generate two reports:

+ Full: a report showing each work with its frequency as in:

    ```
    'call' occurs 1 time.
    'me' occurs 5 times.
    'ishmael' occurs 1 time.
    ...
    ```

+ Summary: a report showing the five most common words and their number of occurences, the five least common words and their number of occurrences.

    ```
    Most common words:
    'the' occurs 14 times
    'and' occurs 9 times
    'i' occurs 9 times
    'of' occurs 8 times
    'is' occurs 7 times

    Least common words:
    'land' occurs 1 times
    'look' occurs 1 times
    'at' occurs 1 times
    'crowds' occurs 1 times
    'watergazers' occurs 1 times
    ```
## [004: replicating wc utility](004_wc_utility/README.md)
> for, files, args

Create a Python program that replicates the basic functionality of the UNIX `wc` utility that reports the number of lines, words, and characters in a file.

In particular, when executing it on the Moby Dick file we get:

```bash
% wc data/moby_01.txt
26 273 1509 data/moby_01.txt
```

Where the output is:
+ The number of lines: 26
+ The number of words: 273
+ The number of characters: 1509

## [005: reactoring word frequency]()

Refactor [003: Calculating the frequency of words in a text file](#003-calculating-the-frequency-of-words-in-a-text-file) using functions.

Use pytest to confirm the different function execution.