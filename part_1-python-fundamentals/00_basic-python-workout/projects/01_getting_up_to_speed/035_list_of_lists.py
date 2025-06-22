"""Illustrate how to work with list of lists in Python."""


def main() -> None:
    """Application entry point."""
    l1 = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9],
    ]

    # Getting the third element of the first list
    third_element_first_list = l1[0][2]
    print(f"Third element of the first list: {third_element_first_list}")
    assert third_element_first_list == 3  # noqa: PLR2004

    # Getting the first element of the second list
    first_element_second_list = l1[1][0]
    print(f"First element of the second list: {first_element_second_list}")
    assert first_element_second_list == 4  # noqa: PLR2004

    # Getting the second element of the third list
    second_element_third_list = l1[2][1]
    print(f"Second element of the third list: {second_element_third_list}")
    assert second_element_third_list == 8  # noqa: PLR2004



if __name__ == "__main__":
    main()
