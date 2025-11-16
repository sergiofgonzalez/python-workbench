"""Manually triggering iteration on an iterable with an iterable."""


def main() -> None:
    """Application entry point."""
    items = ["item_0", "item_1", "item_2"]

    # iter creates an iterator from an iterable
    iterator = iter(items)

    # pulling items from the iterator manually using next()
    first_item = next(iterator)
    assert first_item == "item_0"

    # pulling second and third item manually using next()
    second_item = next(iterator)
    assert second_item == "item_1"
    third_item = next(iterator)
    assert third_item == "item_2"

    # when elements are exhausted you get a StopIteration exception
    try:
        _ = next(iterator)
    except StopIteration as err:
        print(f"Iteration done: {err=}")

    print("=== PASSED ===")


if __name__ == "__main__":
    main()
