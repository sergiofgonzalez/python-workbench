# Proxy to intercept file write operations

Use the **Proxy** pattern to intercept the calls to write information to disk and add a print statement to understand what is being written.

```python
dst_filename = Path("outfiles") / "out_2.txt"
with dst_filename.open("w") as f:
    f_proxy = WriteProxy(f)
    f_proxy.write("This is a line in a file.\n")
    f_proxy.write("There are many lines like this one.\n")
    f_proxy.write("But this is mine.\n")
    f.write(
        "This line will not show in the terminal, but will be written on file.\n"
    )
```