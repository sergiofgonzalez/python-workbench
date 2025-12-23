# 009: refactoring word frequency with modules
> using modules to distribute the functions used to refactor the word frequency program

## Solution

In this refactored version, you just need to create different modules in which you will put all the functions that were present in `main.py`. That will facilitate maintenance.

For the module creation, as you don't intend to reuse anything beyond this program, it is sufficient to create a directory and then place .py files in it:

```
utils/
├── __init__.py  -> package initialization
├── counting.py  -> counting utilities (get_word_count, top_n_*)
├── normalize.py -> text normalization utilities
└── reporting.py -> reporting utilities
```

Then, you just need to move the corresponding functions.


#### tests

The tests just need a little refactoring to reflect we have different modules.

## Running the program

See [README.md](../README.md#009-reactoring-word-frequency-using-modules) for full details.

You can run the application with:

```bash
$ uv run main.py
```

