# 005: refactoring word frequency
> using functions to structure and refactor an existing program

## Solution

### main_v0

The first refactoring attempt introduces functions without changing the program execution flow much. The goal for this first version is to create functions that are responsible for specific portions of the existing program.

As a result, we get, `normalize_text_line()` which abstracts away all the translation and stripping of punctuation, transformation of the words into lowercase, stripping of spaces and splitting into words.

```python
def normalize_text_line(line: str) -> list[str]:
    translation_table = str.maketrans("", "", string.punctuation)
    normalized_line = line.lower().strip()
    normalized_line = normalized_line.translate(translation_table)
    return normalized_line.split()
```

We can also define simple functions for the reports (both full and summary):

```python
def print_full_report(word_count: dict[str, int]) -> None:
    """Prints a full report of word counts."""
    for word, count in word_count.items():
        print(f"{word!r} occurs {count} time{'s' if count != 1 else ''}.")


def print_summary_report(word_count: dict[str, int]) -> None:
    """Prints a summary report of word counts."""
    print("\nSummary Report")
    print("---------------")
    sorted_word_counts = sorted(
        word_count.items(),
        key=lambda item: item[1],
    )

    print("Most common words:")
    # Get last five items in reverse order
    for word, count in sorted_word_counts[:-6:-1]:
        print(f"{word!r} occurs {count} time{'s' if count != 1 else ''}.")

    print("\nLeast common words:")
    for word, count in sorted_word_counts[:5]:
        print(f"{word!r} occurs {count} time{'s' if count != 1 else ''}.")
```

That let us simplify the `main()` function:

```python
def main() -> None:
    """Application entry point."""
    word_count: dict[str, int] = {}
    with (
        in_file_path.open("r", encoding="utf-8") as in_file,
        out_file_path.open("w", encoding="utf-8") as out_file,
    ):
        for line in in_file:
            words = normalize_text_line(line)
            for word in words:
                out_file.write(f"{word}\n")
                word_count[word] = word_count.get(word, 0) + 1

    # Analysis complete
    print_full_report(word_count)
    print_summary_report(word_count)
```

This makes the `main()` very efficient but you can see that it is a little busy:
+ You have the file management (read/write)
+ You have two nested loops to iterate over the lines, then over the words
+ You are accomplishing non-interrelated responsibilities: writing the normalized output file and also counting the words.

While this solution is probably the most efficient, it is more difficult to understand, maintain, and test. Having a `main()` program that simply orchestrates calls to functions will ensure better maintainability.

### main_v1

`main_v1` is the realization of a deeper refactoring of the program to simplify main. Note that in this implementation, some microoptimizations might be lost in favor of maintainability.

The main function is a sequential orchestration of high-level functions:

```python
def main() -> None:
    normalize_text_file(in_file_path, out_file_path)
    word_count = get_word_count(out_file_path)
    print_full_report(word_count)
    print_summary_report(word_count)
```

You clearly see what you want to accompplish:
1. First you normalize a text file, creating an output file as a result.
1. Then, you take the normalized file and get the word count from it.
1. Afterwards, you just use the word count to print the full and summary reports.

Let's start with `normalize_text_file`:

```python
def normalize_text_file(in_file_path: Path, out_file_path: Path) -> None:
    with (
        in_file_path.open("r", encoding="utf-8") as in_file,
        out_file_path.open("w", encoding="utf-8") as out_file,
    ):
        for line in in_file:
            words = normalize_text_line(line)
            for word in words:
                out_file.write(f"{word}\n")
```

You open the input and output file and start reading line by line. For each line, you normalize the line using `normalize_text_line` which returns a line with all the words stripped from punctuation and in lowercase. Then you iterate over each word writing every word on its line.

The function `normalize_text_line()` its the same as before.

```python
def normalize_text_line(line: str) -> list[str]:
    translation_table = str.maketrans("", "", string.punctuation)
    normalized_line = line.lower().strip()
    normalized_line = normalized_line.translate(translation_table)
    return normalized_line.split()

```

The function `get_word_count()` gets the path of the normalized file path and returns a dictionary in which the key is every word found in the file and the value is the number of occurrences for that word:

```python
def get_word_count(in_normalized_file_path: Path) -> dict[str, int]:
    word_count: dict[str, int] = {}
    with in_normalized_file_path.open("r", encoding="utf-8") as in_file:
        for word in in_file:
            stripped_word = word.strip()
            word_count[stripped_word] = word_count.get(stripped_word, 0) + 1
    return word_count
```

Then, `print_full_report()` simply prints the `word_count` dictionary content:

```python
def print_full_report(word_count: dict[str, int]) -> None:
    for word, count in word_count.items():
        print(f"{word!r} occurs {count} time{'s' if count != 1 else ''}.")
```

The only interesting addition is that it checks whether plural or singular should be used for the number of occurrences found.


The summary report is a bit more contrived, as it now relies on functions to get the top most and least common words. Those functions might come in handy if we enhance the program letting the user decide how many words to get:

```python
def print_summary_report(word_count: dict[str, int], num_words: int = 5) -> None:
    print("\n=== Summary Report ===")
    most_common_words = get_top_n_most_common_words(word_count, num_words)
    least_common_words = get_top_n_least_common_words(word_count, num_words)
    print("\nMost common words:")
    for word, count in most_common_words:
        print_word_count(word, count)
    print("\nLeast common words:")
    for word, count in least_common_words:
        print_word_count(word, count)
```

To get the most common words, you just need to use `sorted()` to get a list of tuples where the first element is the word and the second is the number of occurrences. Then, you just use simple slicing to return the top n:

```python
def get_top_n_most_common_words(
    word_count: dict[str, int],
    n: int,
) -> list[tuple[str, int]]:
    sorted_word_counts = sorted(
        word_count.items(),
        key=lambda item: item[1],
        reverse=True,
    )
    return sorted_word_counts[:n]
```

Similarly for the least common words. Note that we're sorting again. If we had to optimize the solution this would probably be the first point to address as we're sorting the `word_count` twice in a very similar fashion:

```python
def get_top_n_least_common_words(
    word_count: dict[str, int],
    n: int,
) -> list[tuple[str, int]]:
    sorted_word_counts = sorted(
        word_count.items(),
        key=lambda item: item[1],
    )
    return sorted_word_counts[:n]
```

Finally, we use a convenience function `print_word_count()` to avoid repeating the print statement for each of the most/least common word entries:

```python
def print_word_count(word: str, count: int) -> None:
    print(f"{word!r} occurs {count} time{'s' if count != 1 else ''}.")
```

#### tests

The tests functions are interesting, as there's interaction with stdout for the reports and the file system for reading, and writing files.

You need to create at least one test function per function in your program.

Let's start with `normalize_text_file()`:

```python
def test_normalize_text_file() -> None:
    sample_input = "Hello, World!\nThis is a test.\n"
    expected_output = ["hello", "world", "this", "is", "a", "test"]
    mock_in_file = mock_open(read_data=sample_input)
    mock_out_file = mock_open()

    def open_side_effect(mode: str, *args: object, **kwargs: object) -> MagicMock:  # noqa: ARG001
        """Return different mock based on file open mode."""
        if mode == "r":
            return mock_in_file()
        return mock_out_file()

    with patch.object(Path, "open", side_effect=open_side_effect):
        normalize_text_file(Path("dummy_input.txt"), Path("dummy_output.txt"))

    # Retrieve the written data from the mock output file
    written_data = []
    handle = mock_out_file()
    handle.write.assert_called()  # Ensure write was called
    for call in handle.write.call_args_list:
        written_data.append(call.args[0].strip())  # noqa: PERF401

    assert written_data == expected_output
```

All the tests should follow the triple-A approach: Arrange, Act, Assert &mdash; this is no different.

You start by arranging a sample input and the output expected to be written.

Then you create two mocks for the files you will open. `mock_open()` is a mock defined in `unittest.mock` that helps you with that.

```python
mock_in_file = mock_open(read_data=sample_input)
mock_out_file = mock_open()
```

See how you need to use it once for the input file, and another one for the output file. In the input file invocation you use `read_data` parameter to identify what is the file suppose to have.

Then, you define the side effect function with which you will configure the invocation to `normalize_text_file`:

```python
def open_side_effect(mode: str, *args: object, **kwargs: object) -> MagicMock:  # noqa: ARG001
    """Return different mock based on file open mode."""
    if mode == "r":
        return mock_in_file()
    return mock_out_file()
```

Note that you receive the `mode` and depending on that you return the input file mock or the output file mock.

Afterwards, you just use the context manager with `patch.object` to mock `Path.open`. This is the Act part.

```python
with patch.object(Path, "open", side_effect=open_side_effect):
    normalize_text_file(Path("dummy_input.txt"), Path("dummy_output.txt"))
```

The final part is the assert part:

```python
written_data = []
handle = mock_out_file()
handle.write.assert_called()  # Ensure write was called
for call in handle.write.call_args_list:
    written_data.append(call.args[0])  # noqa: PERF401

assert written_data == expected_output
```

First, you assert that `write()` has been called in the mock. For that, you just need to use `mock_out_file().write.assert_called()`.

Then, you inspect the arguments list for `write()`, appending all the calls made to `write()` in `written_data`, and then asserting it is the same as the expected output: one single word per line.


Next is `test_normalize_text_line()`. This is a very simple test, that goes through various scenarios to validate we're normalizing the text lines correctly.

```python
def test_normalize_text_line() -> None:
    test_cases = [
        ("Hello, World!", ["hello", "world"]),
        ("  Leading and trailing spaces  ", ["leading", "and", "trailing", "spaces"]),
        (
            "Punctuation! Should; be: removed.",
            ["punctuation", "should", "be", "removed"],
        ),
        ("Mixed CASE Words", ["mixed", "case", "words"]),
        ("Numbers 123 and symbols #@$%", ["numbers", "123", "and", "symbols"]),
        ("", []),
        ("   ", []),
    ]

    for input_line, expected_output in test_cases:
        assert normalize_text_line(input_line) == expected_output
```

You use a list of tuples, where the first element is the input string, and the second element of the tuple is the expected normalized list of words.

Then you run it over `normalize_text_line` asserting the behavior.

Then you test the `get_word_count()`. Again, you will have to rely on `mock_open()`, only that this time, we use the decorator instead of the context manager.

```python
@patch.object(Path, "open")
def test_get_word_count(mock_path_open: MagicMock) -> None:
    """Test the get_word_count function using mocks for file reading."""
    sample_text = "apple\nbanana\napple\ncherry\nbanana\ndate\nelderberry\napple\n"
    expected_word_count = {
        "apple": 3,
        "banana": 2,
        "cherry": 1,
        "date": 1,
        "elderberry": 1,
    }
    mock_path_open.side_effect = mock_open(read_data=sample_text)
    word_count = get_word_count(Path("dummy_path.txt"))
    assert word_count == expected_word_count
```

You configure the `@patch.object` decorator to act on `Path.open()`, and configure the function to receive the `mock_path_open` mock. Then define the sample and expected word count and configure the side effect for the mock.

After that, you just invoke the `get_word_count()` and assert the results.

Another interesting technique is demonstrated in `test_print_full_report()`. In this test, we use a mock named `capfd` to capture the print statements that write to the stdout:

```python
def test_print_full_report(capfd: MagicMock) -> None:
    word_count = {
        "apple": 2,
        "banana": 1,
        "cherry": 3,
    }
    expected_outputs = [
        "'apple' occurs 2 times.",
        "'banana' occurs 1 time.",
        "'cherry' occurs 3 times.",
    ]

    print_full_report(word_count)
    captured = capfd.readouterr()
    output_lines = captured.out.strip().splitlines()

    for expected_line in expected_outputs:
        assert expected_line in output_lines
```

The approach is quite simple:
1. You invoke `print_full_report()`.
1. Then, you use `capfd.readouterr()` to capture the stdout/stderr
1. Afterwards, you give some structure to the string received and then compare it with the expected outputs.

The remaining test functions do not have any new techniques.

## Running the program

See [README.md](../README.md#005-reactoring-word-frequency) for full details.

You can run the application with:

```bash
# v0 with the initial refactoring
$ uv run main_v0.py

# v1 with the initial refactoring
$ uv run main_v1.py
```

