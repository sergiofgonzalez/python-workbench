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

## [005: reactoring word frequency](005_word_frequency_text_file_refactored/README.md)
> for, files, args, functions, pytest, mocks

Refactor [003: Calculating the frequency of words in a text file](#003-calculating-the-frequency-of-words-in-a-text-file) using functions.

Use pytest to confirm the different function execution.

## [006: Hello, modules!](006_hello_modules/README.md)
> modules, pytest, import

Modules are used to organize larger Python projects.

A module is a file containing code. It defines a group of Python functions or other objects under a name which is derived from the name of the file.

Modules help avert name-clash related problems. For example, with modules you can have two functions with the same name (e.g., `my_fn()`), which you will refer as: `module1.my_fn` and `module2.my_fn`. This is possible because each module creates its own namespace, which is essentially a dictionary of identifiers available to use.

Create a simple module named `mymath` on a file named `mymath.py` that:
1. Defines the variable `pi` with value 3.14159.
1. Defines the function `area(r)` which returns the area of the circle with radius `r`.

Then, in your main program, import the recently created module and verify:
1. That you need to qualify the functions and variables' names to use them.
1. That you can ask for specific names from a module to be imported using `from {module} import {name}`.
1. That you can have both `import {module}` and `from {module} import {name}`.


| NOTE: |
| :---- |
| Within the module you can access other definitions without having to qualify the name (e.g., you can use `pi` in the `area()` function without any qualification). |

### [007: Hello, import!](007_hello_import/README.md)
> import, modules, __all__

There are three variants of the `import` statement:
1. `import modulename`
1. `from modulename import name1, name2, name3, ...`
1. `from modulename import *`

The last form brings into use all the exported names in `modulename`, that is those that don't begin with an `_`.

Also, if a list of names called `__all__` exists in the module or the package's `__init__.py`, those will be the names that are imported.

| NOTE: |
| :---- |
| The last form do not prevent name clashing if two modules define the same name. In practice, you should use either 1 or 2. |

Create a simple module named `mymath` on a directory named `mymath`, where you define a `my_math_thingies.py` file that:
1. Defines the variable `pi` with value 3.14159.
1. Defines the function `area(r)` which returns the area of the circle with radius `r`.
1. Defines a variable `_version` with value "0.1.0"
1. In the `__init__.py` define an `__all__` function that includes only the `area`.

Familiarize yourself with the three forms of import and confirm that when using the third one, you don't get access to `pi` or `_version`.

### [008: Grokking the module search path](#008-grokking-the-module-search-path)
> sys.path, uv, --editable, import, PYTHONPATH

The variable `path` from the `sys` module tells you where exactly Python will look for modules.

`sys.path` is a list of directories that Python will search in order when attempting to execute an `import` statement. This variable is initialized from the environment variable `PYTHONPATH`, if it exists, or from a default value that's dependent on your installation.

In addition, `sys.path` has the directory containing the script inserted as its first element. This lets you determine where the executing Python program is located by inspecting `sys.path[0]`. That is, when you do `python app.py`, `sys.path[0]` will tell you where `app.py` is located.

These facts give you three approaches for where to place your own modules:
1. In one of the directories Python normally searches for modules (such as site-specific directories). This is **NOT** recommended, as this is intended to be used for modules specific to your machine.
1. In the same directory as the program you're executing. This is the recommended option for modules that are associated with a particular program, and don't require any other additional project management techniques.
1. Create directories to hold your modules and modify the `sys.path` variable via `PYTHONPATH` so that it includes the new directories. This is a good option for reusable modules (but it's better to create a package without publishing it) and use editable dependencies.

Create a program that prints the value of `sys.path`. Validate that `sys.path[0]` contains the path where the main executing program is located. What is the value of `PYTHONPATH` in your environment?

Create a dummy module that is supposed to be reusable, and come up with the commands you need to use to import that module using `uv` and `PYTHONPATH`.

### [009: reactoring word frequency using modules](009_word_frequency_modules_refactored/)
> modules, import, pytest

Refactor [005: Calculating the frequency of words in a text file](#005-reactoring-word-frequency) using modules so that the `main.py` program becomes even simpler.

Refactor also the tests to reflect the new program structure.


### [010: script that transforms a number to words](010_num_to_words_script/README.md)
> scripts, shebang, argparse, redirection, stdin

As an illustration of the proper way to structure scripts, so that their functions can be used in other programs, create a program that transforms numbers into the equivalent word representation.

For example:

```
python run n2w.py 19
nineteen
```

Include a test mode that you can try interactively (by typing numbers into stdin and finalizing with a CTRL+D) or by feeding a file:

```bash
./n2w.py --test < n2w.test
```

Test it with:

```
0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22
101 102 103 115 900 999
1,000 1,234 1,234,567
```

use argparse with the following configuration for the arguments:

    parser = argparse.ArgumentParser(usage=__doc__)
    parser.add_argument("number", nargs="*")
    parser.add_argument("-t", "--test", dest="test", action="store_true", default=False, help="Test mode: reads from stdin")

### [011: distributing apps as zip files](011_apps_as_zip_files/README.md)
> zip, distribution

While the current standard way of packaging and distributing Python modules and apps is using packages called *wheels*, you can also distribute your app as a zip file.

This format relies on two facts about Python:

1. If a zip file contains a file named `__main__.py`, Python can use that file as the entry point to the archive and execute the `__main__.py` file directly. In addition, the zip file's contents will be added to `sys.path`, so they are available to be imported and executed by `__main__.py`.

1. Zip files allow arbitrary contents to be added to the beginning of the archive. If you add a shebang line pointing to a Python interpreter, and give the file the needed permissions, the file can become self-contained and executable.

Review the information from [zipapp](https://docs.python.org/3/library/zipapp.html) and create a sample zip that can be distributed as an app.