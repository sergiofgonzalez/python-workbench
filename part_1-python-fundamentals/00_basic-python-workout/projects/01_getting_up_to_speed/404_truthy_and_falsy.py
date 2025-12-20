"""Illustrates truthy and falsy values in Python."""


def main() -> None:  # noqa: C901, PLR0912, PLR0915
    """Application entry point."""
    n = 0
    if n:
        print(f"{n} is truthy")
    else:
        print(f"{n} is falsy")

    n = 0.0
    if n:
        print(f"{n} is truthy")
    else:
        print(f"{n} is falsy")

    n = 0 + 0j
    if n:
        print(f"{n} is truthy")
    else:
        print(f"{n} is falsy")

    n = 1
    if n:
        print(f"{n} is truthy")
    else:
        print(f"{n} is falsy")
    print("=" * 40)

    s = ""
    if s:
        print(f"'{s}' is truthy")
    else:
        print(f"'{s}' is falsy")
    s = "Hello"
    if s:
        print(f"'{s}' is truthy")
    else:
        print(f"'{s}' is falsy")
    print("=" * 40)

    lst = []
    if lst:
        print(f"{lst} is truthy")
    else:
        print(f"{lst} is falsy")

    lst = [1, 2, 3]
    if lst:
        print(f"{lst} is truthy")
    else:
        print(f"{lst} is falsy")

    d = {}
    if d:
        print(f"{d} is truthy")
    else:
        print(f"{d} is falsy")

    d = {"a": 1, "b": 2}
    if d:
        print(f"{d} is truthy")
    else:
        print(f"{d} is falsy")

    s = set()
    if s:
        print(f"{s} is truthy")
    else:
        print(f"{s} is falsy")

    s = {1, 2, 3}
    if s:
        print(f"{s} is truthy")
    else:
        print(f"{s} is falsy")

    print("=" * 40)
    x = None
    if x:
        print(f"{x} is truthy")
    else:
        print(f"{x} is falsy")


if __name__ == "__main__":
    main()
