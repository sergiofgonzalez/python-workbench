# Hello CLI tool using `click`
> Simple program that outputs a greeting for a certain number of times

## Usage

```bash
$ python hello.py --name "Jason Isaacs" --count 3
Hello to Jason Isaacs!
Hello to Jason Isaacs!
Hello to Jason Isaacs!
```

Note how with very little effort you get a lot of out-of-the-box capabilities:


For example, you get help from the info found in your function and decorator attributes:

```bash
$ python hello.py --help
Usage: hello.py [OPTIONS]

  Simple program that greets NAME for a total COUNT times.

Options:
  --count INTEGER  Number of greetings.
  --name TEXT      The person to greet.
  --help           Show this message and exit.
```

And the tool can prompt the user for the required options:
```bash```
$ python hello.py
Your name:
```