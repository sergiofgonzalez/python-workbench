# Gzipping a file using buffer mode

Illustrates how to create a .gz of a file using a buffer mode. That is, the contents of the input file are read and materialized in a buffer before they are compressed.

You can create arbitrarily big files using:

```bash
# Create a 100MB file
dd if=/dev/urandom of=bigfile.bin bs=1M count=100
```