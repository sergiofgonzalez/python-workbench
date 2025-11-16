"""Illustrates how to find items in sequences."""


def main() -> None:
    """Application entry point."""
    nums = [1, 2, 3, 4, 5]
    assert (8 in nums) is False  # noqa: PLR2004
    assert (4 in nums) is True  # noqa: PLR2004
    loc_of_4 = nums.index(4)
    assert loc_of_4 == 3  # noqa: PLR2004
    try:
        loc_of_8 = nums.index(8)  # noqa: F841
    except ValueError as err:
        print(f"Error: {err}")
    print("=== PASSED ===")

    s = "Python is cool!"
    assert ("cool" in s) is True
    loc_of_cool = s.index("cool")
    assert loc_of_cool == 10  # noqa: PLR2004
    loc_of_cool = s.find("cool")
    assert loc_of_cool == 10  # noqa: PLR2004
    loc_of_rust = s.find("rust")
    assert loc_of_rust == -1
    print("=== PASSED ===")

    t = (404, "Page Not Found")
    assert (404 in t) is True  # noqa: PLR2004
    assert ("Not" in t) is False
    loc_of_404 = t.index(404)
    assert loc_of_404 == 0
    print("=== PASSED ===")



if __name__ == "__main__":
    main()
