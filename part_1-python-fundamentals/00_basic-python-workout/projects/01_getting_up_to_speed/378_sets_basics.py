"""Basic set operations."""


def main() -> None:
    """Application entry point."""
    assert set([1, 2, 3, 4, 5]) == {1, 2, 3, 4, 5}  # noqa: C405

    x = {1, 2, 3, 4, 5}
    x.add(6)
    assert x == {1, 2, 3, 4, 5, 6}

    x = {1, 2, 3, 4, 5}
    x.add(3)
    assert x == {1, 2, 3, 4, 5}

    x = {1, 2, 3, 4, 5}
    x.remove(5)
    assert x == {1, 2, 3, 4}

    x = {1, 2, 3, 4, 5}
    try:
        x.remove(6)
    except KeyError as exc:
        print(f"Caught expected exception: {exc}")

    assert 1 in {1, 2, 3, 4, 6}
    assert 5 not in {1, 2, 3, 4, 6}  # noqa: PLR2004

    assert {1, 2, 3, 4, 6} | {1, 7, 8, 9} == {1, 2, 3, 4, 6, 7, 8, 9}  # union

    assert {1, 2, 3, 4, 6} & {1, 7, 8, 9} == {1}  # intersection

    assert {1, 2, 3, 4, 6} ^ {1, 7, 8, 9} == {2, 3, 4, 6, 7, 8, 9}  # xor

if __name__ == "__main__":
    main()
