"""Illustrate the basics of list slicing."""


def main() -> None:
    """Application entry point."""
    nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    # sublist from the 2nd to the 5th element (inclusive)
    sublist = nums[1:5]
    print(f"Sublist from 2nd to 5th element: {sublist}, length: {len(sublist)}")
    assert len(sublist) == 4  # noqa: PLR2004
    assert sublist == [2, 3, 4, 5]

    # sublist from the 2nd to the one before last element
    sublist = nums[1:-1]
    print(
        f"Sublist from 2nd to one before last element: {sublist}, length: {len(sublist)}"
    )
    assert len(sublist) == 8  # noqa: PLR2004
    assert sublist == [2, 3, 4, 5, 6, 7, 8, 9]

    # sublist from the 2nd to the last element
    sublist = nums[1:]
    print(f"Sublist from 2nd to last element: {sublist}, length: {len(sublist)}")
    assert len(sublist) == 9  # noqa: PLR2004
    assert sublist == [2, 3, 4, 5, 6, 7, 8, 9, 10]

    # sublist from the first to the one before last element
    sublist = nums[:-1]
    print(
        f"Sublist from first to one before last element: {sublist}, length: {len(sublist)}"
    )
    assert len(sublist) == 9  # noqa: PLR2004
    assert sublist == [1, 2, 3, 4, 5, 6, 7, 8, 9]


if __name__ == "__main__":
    main()
