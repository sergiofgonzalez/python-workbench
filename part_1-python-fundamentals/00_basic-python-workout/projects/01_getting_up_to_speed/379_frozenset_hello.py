"""Demonstrate basic usage of frozenset."""


def main() -> None:
    """Application entry point."""
    x = set([1, 2, 3, 1, 3, 5])  # noqa: C405
    z = frozenset(x)
    print(f"Set x: {x}")
    print(f"Frozenset z: {z}")
    print("=" * 40)

    assert x == z
    print(f"x: {x!r:<25}, id={id(x):#x}")
    print(f"z: {z!r:<25}, id={id(z):#x}")

    # We cannot add elements to a frozenset
    try:
        z.add(6)  # type: ignore[attr-defined]
    except AttributeError as exc:
        print(f"Caught expected exception: {exc}")


if __name__ == "__main__":
    main()
