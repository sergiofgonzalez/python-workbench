# 004: replicating `wc` Unix utility
> reimplementing the basic capabilities of `wc` in Python

## Solution

Because the program is the reimplementation of a CLI utility, we start by accessing the arguments sent from the command line:

```python
if len(sys.argv) < 2:  # noqa: PLR2004
    print("Usage: python main.py <filename>")
    sys.exit(1)

filename = sys.argv[1]
```

Then, we initialize the counters for the lines, words, and characters/bytes count and iterate over each line:

```python
line_count = 0
word_count = 0
byte_count = 0
try:
    with Path(filename).open("r", encoding="utf-8") as file:
        for line in file:
            line_count += 1
            word_count += len(line.split())
            byte_count += len(line.encode("utf-8"))  # Count bytes in UTF-8 encoding
except FileNotFoundError:
    print(f"{filename}: No such file")
    sys.exit(1)
```

Finally, we simply print a line with the report:

```python
print(f"{line_count} {word_count} {byte_count} {filename}")code
```


## Running the program

See [README.md](../README.md#004-replicating-wc-utility) for full details.

You can run the application with:

```bash
uv run main.py data/moby_01.txt
```
