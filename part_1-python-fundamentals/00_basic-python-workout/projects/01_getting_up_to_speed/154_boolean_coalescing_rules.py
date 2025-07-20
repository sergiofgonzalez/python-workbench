"""Illustrate boolean coalescing rules."""


def main() -> None:  # noqa: C901, PLR0912, PLR0915
    """Application entry point."""
    # numbers are truthy except 0
    num = 0
    if num:
        print(f"Number {num} is truthy")
    else:
        print(f"Number {num} is falsy")

    num = 42
    if num:
        print(f"Number {num} is truthy")
    else:
        print(f"Number {num} is falsy")

    # strings are truthy except empty string
    text = ""
    if text:
        print(f"String '{text}' is truthy")
    else:
        print(f"String '{text}' is falsy")

    text = "Hello"
    if text:
        print(f"String '{text}' is truthy")
    else:
        print(f"String '{text}' is falsy")

    # lists are truthy except empty list
    lst = []
    if lst:
        print(f"List {lst} is truthy")
    else:
        print(f"List {lst} is falsy")

    lst = [1, 2, 3]
    if lst:
        print(f"List {lst} is truthy")
    else:
        print(f"List {lst} is falsy")

    # dictionaries are truthy except empty dictionary
    dct = {}
    if dct:
        print(f"Dictionary {dct} is truthy")
    else:
        print(f"Dictionary {dct} is falsy")

    dct = {"key": "value"}
    if dct:
        print(f"Dictionary {dct} is truthy")
    else:
        print(f"Dictionary {dct} is falsy")

    # None is falsy
    value = None
    if value:
        print(f"Value {value} is truthy")
    else:
        print(f"Value {value} is falsy")

    # set is truthy except empty set
    s = set()
    if s:
        print(f"Set {s} is truthy")
    else:
        print(f"Set {s} is falsy")

    s = {1, 2, 3}
    if s:
        print(f"Set {s} is truthy")
    else:
        print(f"Set {s} is falsy")

    # tuples are truthy except empty tuple
    t = ()
    if t:
        print(f"Tuple {t} is truthy")
    else:
        print(f"Tuple {t} is falsy")
    t = (1, 2, 3)
    if t:
        print(f"Tuple {t} is truthy")
    else:
        print(f"Tuple {t} is falsy")


if __name__ == "__main__":
    main()
