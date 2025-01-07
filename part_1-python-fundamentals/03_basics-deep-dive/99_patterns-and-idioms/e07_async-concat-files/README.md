# asynchronous file concatenation

Write the implementation of a `concat_files(file_1, file2, ..., dst_file)` that takes two or more paths to text files in the file system and a destination file (the last argument).

The function must copy the contents of every source file into the destination file, respecting the order of the files provided in the argument list. The function must be able to handle any arbitrary number of arguments.

Add some logging to understand whether you're leveraging concurrency. If not, create a second version of the program in which multiple tasks are intertwined so that something is executed while you're waiting for I/O.

## main_v0

First implementation: leverages async await but does leverage any concurrency benefit.

## main_v1

Using `asyncio.gather()` to read the files in parallel.

## main_v2

Using `asyncio.create_task()`.

## main_v3

Using TaskGroup