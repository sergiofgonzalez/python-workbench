"""Illustrates how to use pickle.dumps and pickle.loads."""

import pickle


def say_hello(name: str) -> None:
    """Greets the given user."""
    print(f"Hello to {name}!")


def main() -> None:
    """Application entry point."""
    pickled_function = pickle.dumps(say_hello)
    unpickled_say_hello = pickle.loads(pickled_function)  # noqa: S301
    unpickled_say_hello("Alice")

    # it's the same function!
    assert say_hello == unpickled_say_hello
    assert say_hello is unpickled_say_hello

    print(f"say_hello id: {id(say_hello):#x}")
    print(f"unpickled id: {id(unpickled_say_hello):#x}")

if __name__ == "__main__":
    main()
