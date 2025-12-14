"""Illustrates how to do custom sorting."""


def main() -> None:
    """Application entry point."""
    lst = ["uno", "dos", "tres", "cuatro", "cinco"]

    # sort by length of the string
    lst.sort(key=len)
    print(lst)
    assert lst == ["uno", "dos", "tres", "cinco", "cuatro"]

    lst = ["uno", "tres", "cuatro"]

    # sort by length of the string in reverse order
    lst.sort(key=len, reverse=True)
    print(lst)
    assert lst == ["cuatro", "tres", "uno"]

    lst = [[1, 2, 3], [2, 1, 3], [4, 0, 1]]
    # sort by the second element of each sub-list
    lst.sort(key=lambda x: x[1])
    print(lst)
    assert lst == [[4, 0, 1], [2, 1, 3], [1, 2, 3]]

if __name__ == "__main__":
    main()
