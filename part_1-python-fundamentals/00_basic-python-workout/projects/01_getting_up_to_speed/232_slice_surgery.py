"""Illustrate slice surgery (wizardry!) techniques."""


def main() -> None:
    """Application entry point."""
    nums = list(range(9))
    print(f"Original list: {nums}")

    # mutate the three first elements of the list with [10, 11, 12]
    nums[:3] = [10, 11, 12]
    assert nums == [10, 11, 12, 3, 4, 5, 6, 7, 8]

    # mutate from the 4th element to the end with [13, 14, 15, 16, 17, 18, 19, 20]
    nums[3:] = list(range(13, 21))
    assert nums == [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]

    # mutate and shrink the list so that the resulting list
    # is [0, 1, 15, 16, 17, 18, 19, 20]
    nums[:5] = [0, 1]
    assert nums == [0, 1, 15, 16, 17, 18, 19, 20]

    print("=== PASSED ===")
    nums = [0, 1, 0, 16, 0, 18, 0, 20]
    print(f"Original list: {nums}")

    # remove the elements from the beginning until the 3rd using del
    del nums[:4]
    assert nums == [0, 18, 0, 20]

    # remove the elements from the 2nd before the last to the end using empty list
    nums[-2:] = []
    assert nums == [0, 18]
    print("=== PASSED ===")


if __name__ == "__main__":
    main()
