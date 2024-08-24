# fileinput module
> illustrating how to iterate over file contents using the `fileinput` module

## Running the application

### Script1: `fileinput.input()` basics

To see the script1 in action, type:

```bash
python script1.py infile_1.txt infile_2.txt
```

You will get the output of both files, where the lines starting with `#` have been removed.

If no arguments are provided, the stdin will be captured, and each line will be passed to the script as it is being written:

```bash
$ python script1.py
This is a line
>> This is a line
# this is a comment line
this is another line
>> this is another line
^D
```

You can terminate the stdin by typing CTRL+D.

### Script2: Additional `fileinput` functions

This script illustrates some additional `fileinput` functions that help identify the file that is being read and the line number from each file.

```bash
python script2.py infile_1.txt infile_2.txt
<start of file infile_1.txt>
 | 1 | 1  >> this is the first line of the file.
 | 2 | 2  >> this is the second line of the files.
 | 4 | 4  >> this file has many lines but this one is mine.
<start of file infile_2.txt>
 | 5 | 1  >> this is another line in another file.
 | 6 | 2  >> and some numbers:
 | 7 | 3  >> 12 15 0
 | 9 | 5  >> 100 100 0
```

You can also invoke it without arguments to read from stdin:

```bash
$ python script2.py
This is a line
<start of file <stdin>>
<stdin> | 1 | 1  >> This is a line
This is another line
<stdin> | 2 | 2  >> This is another line
```

### Script3: Setting the files from which you read from

The third script illustrates how you can pass the a file or a list of files to `fileinput.input()` instead of taking them from `sys.argv`.