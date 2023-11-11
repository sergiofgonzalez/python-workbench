"""Main program (not main CLI app)"""
from hellopkg.utils import generate_greeting


def get_greeting(name):
    greeting = generate_greeting(name)
    return greeting


if __name__ == "__main__":
    print("Not supposed to be run like this: use the CLI tool")
