"""Entry point for the application."""
from prgtotest.mylibtotest import add

if __name__ == "__main__":
    print(add(1, 2))
    print(add(1.1, 2.2))
    print(add("1", "2"))
