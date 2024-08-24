# Dealing with command line options with `argparse`
> illustrates `argparse.ArgumentParser` features

## Running the script

The application requires two positional arguments:
+ argument 1: `indent`, an int
+ argument 2: `input_file`

And several optional arguments that must come before the positional ones:
+ `-f`
+ `-x`
+ `-q`

You can type:

```bash
$ python script.py -x100 -q -f outfile 2 arg2
arguments: Namespace(indent=2, input_file='arg2', filename='outfile', xray='100', verbose=False)
```

When `-q` is not given, `verbose=True`. When given, `verbose=False`.