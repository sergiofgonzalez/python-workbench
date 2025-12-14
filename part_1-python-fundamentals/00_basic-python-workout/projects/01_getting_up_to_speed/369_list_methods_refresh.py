"""Checking your list methods skills."""


def main() -> None:  # noqa: PLR0915
    """Application entry point."""
    # [1, 2, 3].append(4) -> [1, 2, 3, 4]
    lst = [1, 2, 3]
    lst.append(4)
    assert lst == [1, 2, 3, 4]

    # [1, 2, 3].clear() -> []
    lst = [1, 2, 3]
    lst.clear()
    assert lst == []

    # [1, 2, 3].copy() -> [1, 2, 3]
    lst = [1, 2, 3]
    assert lst.copy() == [1, 2, 3]

    # [1, 2, 3].count(2) -> 1
    lst = [1, 2, 3]
    assert lst.count(2) == 1

    # [1, 2, 3].extend([4, 5]) -> [1, 2, 3, 4, 5]
    lst = [1, 2, 3]
    lst.extend([4, 5])
    assert lst == [1, 2, 3, 4, 5]

    # [1, 2, 3].index(2) -> 1
    lst = [1, 2, 3]
    assert lst.index(2) == 1

    # [1, 2, 3].insert(1, "a") -> [1, "a", 2, 3]
    lst = [1, 2, 3]
    lst.insert(1, "a") # type: ignore  # noqa: PGH003
    assert lst == [1, "a", 2, 3]

    # [1, 2, 3].pop() -> 3
    lst = [1, 2, 3]
    popped = lst.pop()
    assert popped == 3  # noqa: PLR2004
    assert lst == [1, 2]

    # [1, 2, 3].pop(1) -> 2
    lst = [1, 2, 3]
    popped = lst.pop(1)
    assert popped == 2  # noqa: PLR2004
    assert lst == [1, 3]

    # [1, 2, 3].remove(2) -> [1, 3]
    lst = [1, 2, 3]
    lst.remove(2)
    assert lst == [1, 3]

    # [1, 2, 3].reverse() -> [3, 2, 1]
    lst = [1, 2, 3]
    lst.reverse()
    assert lst == [3, 2, 1]

    # [1, 2, 3].sort() -> [1, 2, 3]
    lst = [3, 1, 2]
    lst.sort()
    assert lst == [1, 2, 3]

    # [1, 2, 3].sort(reverse=True) -> [3, 2, 1]
    lst = [1, 2, 3]
    lst.sort(reverse=True)
    assert lst == [3, 2, 1]

    # [1, 2, 3] + [4, 5] -> [1, 2, 3, 4, 5
    lst = [1, 2, 3] + [4, 5]  # noqa: RUF005
    assert lst == [1, 2, 3, 4, 5]

    # [1, 2, 3] * 2 -> [1, 2, 3, 1, 2, 3]
    lst = [1, 2, 3] * 2
    assert lst == [1, 2, 3, 1, 2, 3]

    # [1, 2, 3][1] -> 2
    lst = [1, 2, 3]
    assert lst[1] == 2  # noqa: PLR2004

    # [1, 2, 3][:2] -> [1, 2]
    lst = [1, 2, 3]
    assert lst[:2] == [1, 2]

    # [1, 2, 3][1:] -> [2, 3]
    lst = [1, 2, 3]
    assert lst[1:] == [2, 3]

    # len([1, 2, 3]) -> 3
    lst = [1, 2, 3]
    assert len(lst) == 3  # noqa: PLR2004

    # [1, 2, 3].append(4) -> [1, 2, 3, 4]
    lst = [1, 2, 3]
    lst.append(4)
    assert lst == [1, 2, 3, 4]

    # [x * 2 for x in [1, 2, 3]] -> [2, 4, 6]
    lst = [x * 2 for x in [1, 2, 3]]
    assert lst == [2, 4, 6]

    # list("abc") -> ["a", "b", "c"]
    lst = list("abc")
    assert lst == ["a", "b", "c"]

    # list(range(3)) -> [0, 1, 2]
    lst = list(range(3))
    assert lst == [0, 1, 2]

    # sum([1, 2, 3]) -> 6
    lst = [1, 2, 3]
    total = sum(lst)
    assert total == 6  # noqa: PLR2004

    # max([1, 2, 3]) -> 3
    lst = [1, 2, 3]
    assert max(lst) == 3  # noqa: PLR2004

    # min([1, 2, 3]) -> 1
    lst = [1, 2, 3]
    assert min(lst) == 1

    # any([False, True, False]) -> True
    lst = [False, True, False]
    assert any(lst) is True

    # all([True, True, True]) -> True
    lst = [True, True, True]
    assert all(lst) is True

    # sorted([3, 1, 2]) -> [1, 2, 3]
    lst = [3, 1, 2]
    sorted_lst = sorted(lst)
    assert sorted_lst == [1, 2, 3]
    assert lst == [3, 1, 2]

    # list(enumerate(["a", "b"])) -> [(0, "a"), (1, "b")]
    lst = list(enumerate(["a", "b"]))
    assert lst == [(0, "a"), (1, "b")]

    # list(map(str, [1, 2, 3])) -> ["1", "2", "3"]
    lst = list(map(str, [1, 2, 3]))
    assert lst == ["1", "2", "3"]

if __name__ == "__main__":
    main()
