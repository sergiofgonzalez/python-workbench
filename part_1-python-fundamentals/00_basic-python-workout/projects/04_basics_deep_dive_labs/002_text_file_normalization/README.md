# 002: normalizing a text file
> normalizing a text file removing punctuation and creating a file that will be used in further processing

In processing raw text, it's often necessary to clean and normalize the text before doing anything else.

For example, if you want to find the frequence of words in a text, it's quite common to normalize before calculating that frequency. It's also common to break the text into a series of words and write each one of them on its own line.

Read the first part of the first chapter of Moby Dick, normalizing it (making sure that everything is using either lowercase or uppercase), remove all punctuation, and write the words one per line to a second file.

## Solution

1. You start by creating a directory to host your project. Because it's a simple program, you can just create a directory and copy a simple `pyproject.toml` well configured from another project. (NOTE: using `uv init` in this type of workspace will update an upstream `pyproject.toml` and complicate things unnecessarily).

The ideal `pyproject.toml` should look like the following:

    ```toml
    [project]
    name = "002-text_file_normalization"
    version = "0.1.0"
    description = "Lab2: Normalizing a text file (as a 1st step for further processing)."
    readme = "README.md"
    requires-python = ">=3.12"
    dependencies = []

    [dependency-groups]
    dev = ["ruff>=0.14.8"]

    [tool.ruff]

    ignore = [
      "T201", # Allow print statements
    ]

    # Enable all rules
    select = ["ALL"]

    [tool.ruff.lint.pydocstyle]
    convention = "google"
    ```

  Note that it just features ruff because the project is simple enough and doesn't require tests.

1. Then, you will program the solution in `main.py`. The following sections give you an annotated solution.

1. You start with your imports and global definitions. As you will be reading from file and writing the solution to a file, it's appropriate to define the path for those files:

    ```python
    import string
    from pathlib import Path

    in_file_path = Path("data/moby_01.txt")
    out_file_path = Path("data/moby_01_normalized.txt")
    ```

1. As stated in the solution, you will need to remove all punctuation. The most efficient and Pythonic way to do is to use `str.maketrans()`. Because you won't be changing the translation table in the execution, you can create the translation table at the beginning and then reuse it in your program:

    ```python
    translation_table = str.maketrans("", "", string.punctuation)
    ```

    You should remember that maketrans either use the first two parameters (which then should be used one-to-one mappings), or a third argument that will be used to set all of the characters in that set to `None`. You are using that third argument to remove all punctuation.

1. Then you open the input and output files:

    ```python
        with (
            in_file_path.open("r", encoding="utf-8") as in_file,
            out_file_path.open("w", encoding="utf-8") as out_file,
        ):
    ```

    Note how we're clubbing the opening of the input file, and the opening of the output file in the same context.

1. Then, you just need to process the contents of the input file. This fill feature lines of text that you will have to process. Because the file can be large, rather than using `read()` or `readlines()` you should process line by line. It is possible that it is less quick than using `read()` and `readlines()` but it will definitely be less memory hungry and will make the processing easier to reason about. Thus, you can do:


    ```python
    for line in in_file:
      # ... processing here ..
    ```

1. Now, you just need to make the normalization. Namely:
    1. Transform each line to lowercase, removing the extra characters at the beginning or end using `strip()`.
    1. Using the `translate()` method with our `translation_table` to remove all punctuation (those characters such as '.', '-', etc. will be replaced by `None`).
    1. Using `split()` to get a list of strings for each line. Because you have already removed all punctuation, it's safe to split by space.
    1. Then, you just iterate over each of the words of that string and write it to the output file:


    ```python
    for line in in_file:
      normalized_line = line.lower().strip()
      normalized_line = normalized_line.translate(translation_table)
      words = normalized_line.split()
      for word in words:
          out_file.write(f"{word}\n")
    ```

## Running the program

You can run the application with:

```bash
uv run main.py
```

