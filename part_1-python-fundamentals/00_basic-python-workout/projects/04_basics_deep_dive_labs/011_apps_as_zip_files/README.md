# 011: distributing apps as zip files
> illustrates how to distribute an app as a zip file

## Solution

As explained in the exercise's problem statement, you can distribute a script in a zip file.

Again, this seems to be a little hacky when compared with distributing packages published in PyPI, but it's worth trying.

First, you need to rename the script as `__main__.py`.

```bash
$ cp n2w.py __main__.py
```

Then, you need to create a zip with that file. If you don't have `zip` installed, you will have to do `apt install zip`:

```bash
# update packages
$ sudo apt update

# install zip
$ sudo apt install zip

# create a zip file with __main__.py in it
$zip n2w.zip __main__.py
```

Now, it's ready to be executed, even with `uv`:

```bash
$ uv run n2w.zip
Namespace(number=[], test_mode=False)
```


## Running the program

See [README.md](../README.md#011-distributing-apps-as-zip-files) for full details.


To run the script you can use the same options as in [n2w](../010_num_to_words_script/README.md#running-the-program):

You can run the application in many different ways

```bash
# do nothing
$ uv run n2w.zip

# show help
$ uv run n2w.zip --help

# run with a single number
$ uv run n2w.zip 1,010,123

# run with several numbers
$ uv run n2w.zip 1 2 3

# run in test mode with user typing into stdin
$ uv run n2w.zip --test
Namespace(number=[], test_mode=True)
Test mode enabled. Reading numbers from stdin...
1
2
3
14
1 = one
2 = two
3 = three
14 = fourtee

# run in test mode by passing a file
$ uv run n2w.zip --test < n2w_test.txt
```

