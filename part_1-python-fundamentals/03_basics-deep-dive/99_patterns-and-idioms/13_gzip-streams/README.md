# Gzipping a file using stream mode

Illustrates how to create a .gz of a file using stream mode. That is, the contents of the input file are streamed to the compressed file before the input file is completely read.

You can create arbitrarily big files using:

```bash
# Create a 100MB file
dd if=/dev/urandom of=bigfile.bin bs=1M count=100
```

## main_v0

Using regular files and `gzip.compress()`.

NOTE: this version is faster for some reason.

## main_v1

Using `gzip.open()` and `write`.

NOTE: this version is slower for some reason.

## main_v2

Using `aiofiles` and `gzip.compress()`.

## main_v3

A more complicated attempt, running the reading of the next chunk in parallel with the writing of the current chunk, but it ends up being a bit slower.
Using `aiofiles` and `gzip.compress()`.