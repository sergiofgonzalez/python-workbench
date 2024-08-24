# stdin/stdout
> illustrates how to work with `sys.stdin` and `sys.stdout`.

In the script, we read the contents of the stdin into a variable and perform the substitution of `sys.argv[1]` by `sys.argv[2]` in it.

## Running the script

As an example, you can do:

```bash
$ python script.py me I
>This is me writing into stdin
^D
This is I writing into stdin
```

When you execute the script, it will start capturing the standard input, so everything you type will be displayed on screen. When you're done typing you will have to type CTRL+D to signal the end of what you want to send to the script.

Instead of typing directly in the terminal window, you can pass a file to do the substitution:

```bash
python script.py me I < infile.txt
```

You can also pipe the output of a first execution of the script to a subsequent execution of the same script.

```bash
python script.py 0 zero < infile.txt | python script.py 1 one > outfile.txt
```