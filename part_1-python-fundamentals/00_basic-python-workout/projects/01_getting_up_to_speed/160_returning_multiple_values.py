"""Illustrate how to return multiple values in a Python function."""


def foo() -> tuple[int, str, list]:
    """Return multiple values from a function."""
    return 42, "Hello", [1, 2, 3]


def main() -> None:
    """Application entry point."""
    result = foo()
    print(f"Result: {result}")
    print(f"Type of result: {type(result)}")

    num, text, lst = result
    print(f"Number: {num}, Text: {text}, List: {lst}")
    print(
        f"Type of num: {type(num)}, "
        f"Type of text: {type(text)}, "
        f"Type of lst: {type(lst)}",
    )


if __name__ == "__main__":
    main()
