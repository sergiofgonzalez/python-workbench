"""Illustrate the behavior of zip() when using iterables of different size."""


def main() -> None:
    """Application entry point."""
    nums1 = range(3)
    nums2 = ["a", "b", "c", "d"]
    # Default behavior of zip() is to stop at the shortest iterable
    print(list(zip(nums1, nums2)))  # noqa: B905
    assert list(zip(nums1, nums2)) == [(0, "a"), (1, "b"), (2, "c")]  # noqa: B905

    # Using strict=True will raise a ValueError if the iterables are of different lengths
    try:
        print(list(zip(nums1, nums2, strict=True)))
    except ValueError as e:
        print(f"ValueError: {e}")

    # Using strict=False will not raise an error, but will stop at the shortest iterable
    print(list(zip(nums1, nums2, strict=False)))  # noqa: B905


if __name__ == "__main__":
    main()
