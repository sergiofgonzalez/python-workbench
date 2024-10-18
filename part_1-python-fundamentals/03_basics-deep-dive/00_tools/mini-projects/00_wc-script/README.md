# Implementing a portion of `wc` in Python
> final project of the Python Programs chapter illustrating how to build a small CLI tool using the Python standard library capabilities.

## What are we going to build?

`wc` is a small Unix/Linux utility that prints newline, word, and byte counts for each file.

The following is the result of running `wc --help`:

Usage: wc [OPTION]... [FILE]...
  or:  wc [OPTION]... --files0-from=F
Print newline, word, and byte counts for each FILE, and a total line if
more than one FILE is specified.  A word is a non-zero-length sequence of
characters delimited by white space.

With no FILE, or when FILE is -, read standard input.

The options below may be used to select which counts are printed, always in
the following order: newline, word, character, byte, maximum line length.
  -c, --bytes            print the byte counts
  -m, --chars            print the character counts
  -l, --lines            print the newline counts
      --files0-from=F    read input from the files specified by
                           NUL-terminated names in file F;
                           If F is - then read names from standard input
  -L, --max-line-length  print the maximum display width
  -w, --words            print the word counts
      --help     display this help and exit
      --version  output version information and exit

Out of the full `wc` capabilities, our implementation must have options to show only lines (`-l`), only words (`-w`), and only characters (`-c`). If none of these options are given, the three stats are displayed, but if ny of these options are present, only those stats are shown.

Also, if no file is given, our program should be able to read from stdin.

## Exploring `wc` capabilities:

Running `wc` with a single and multiple files looks like the following:

```bash
$ wc README.md
  26  211 1414 README.md

# it works on multiple files too
$ wc README.md wc.py
  33  226 1505 README.md
   0    0    0 wc.py
  33  226 1505 total
```

It's also interesting that:

```bash
$ wc one-line.txt
0 4 17 one-line.txt

# File ends with a line featuring only a "\n"
$ wc one-line-linux.txt
1 4 18 one-line-linux.txt
```

## Implementation Plan and tests

The goal is to replicate *broadly* how `wc` works, taking into account that the idea is getting familiarized with how to build CLI tools with Python's std lib, rather than exactly replicating `wc`.

That said, the implementation plan was:
1. Set up the main scaffolding with a controlling function
2. Using argparse to parse the arguments from the CLI
3. Delegating counting the lines, words, and chars to a generic function
4. Delegating showing the report
5. Comparing results with `wc` and final adjustments (aka manual tests):
  1. No args - must use stdin: OK
  2. Giving only one from `-l`, `-c`, or `-w`, with zero, one and multiple files: OK
  3. Giving only two from `-l`, `-c`, or `-w`, with zero, one and multiple files: OK
  4. Giving three params, with zero, one and multiple files: OK
  5. giving one file and two files: OK
  6. Giving file names that don't exist or no permission: OK
  7. Using arguments not defined: OK
  8. Using path instead of current dir: OK
  9. passing the same file twice: OK
  10. Linux terminated and Windows terminated files: NOT OK, but can't find easy way
