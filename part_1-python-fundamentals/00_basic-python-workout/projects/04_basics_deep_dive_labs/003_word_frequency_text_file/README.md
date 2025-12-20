# 003: Calculating the frequency of words in a text file
> Calculate

## Solution

The first part of the program is identical to [002: normalizing a text file](../002_text_file_normalization/), except for the declaration of `word_count`: a dictionary with string keys and int values that you will use to keep the word frequency information.

```python
def main() -> None:
    """Application entry point."""
    word_count: dict[str, int] = {}
    translation_table = str.maketrans("", "", string.punctuation)
    with (
        in_file_path.open("r", encoding="utf-8") as in_file,
        out_file_path.open("w", encoding="utf-8") as out_file,
    ):
        for line in in_file:
            normalized_line = line.lower().strip()
            normalized_line = normalized_line.translate(translation_table)
            words = normalized_line.split()
            for word in words:
                out_file.write(f"{word}\n")
```

However, while doing the iteration and writing the output file, you can keep the count of the words you've seen so far in `word_count` dictionary by doing:

```python
for word in words:
    out_file.write(f"{word}\n")
    word_count[word] = word_count.get(word, 0) + 1
```

In a very succinct way, using `dict.get()` you:
+ initialize the count of *unseen* words to 1
+ increment by one the count of already seen words


Afterwards, you just print a full report:

```python
for word, count in word_count.items():
    print(f"{word!r} occurs {count} time{'s' if count != 1 else ''}.")
```

And a summary report, that requires a bit of data massaging:

```python
sorted_word_counts = sorted(
    word_count.items(),
    key=lambda item: item[1],
)
```

You use `sorted()` to get a list of tuples sorted by the count number for each word.

Then you just print the most and least common words using slicing:

```python
print("Most common words:")
# Get last five items in reverse order
for word, count in sorted_word_counts[:-6:-1]:
    print(f"{word!r} occurs {count} time{'s' if count != 1 else ''}.")

print("\nLeast common words:")
for word, count in sorted_word_counts[:5]:
    print(f"{word!r} occurs {count} time{'s' if count != 1 else ''}.")
```

Because `sorted_word_counts` is sorted in ascending order, the slicing for the most common words is a bit tricky, while the least common words is trivial.


## Running the program

See [README.md](../README.md#003-calculating-the-frequency-of-words-in-a-text-file) for full details.

You can run the application with:

```bash
uv run main.py
```

