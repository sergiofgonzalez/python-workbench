"""Unit tests for utils (testing only the public interface)."""

import pytest

from typedlist.utils import TypedList


def test_typed_list_initialization() -> None:
    """Test initialization of TypedList with correct and incorrect types."""
    tlist = TypedList(0, [1, 2, 3])
    assert len(tlist) == 3

    tlist = TypedList("example")
    assert len(tlist) == 0

    with pytest.raises(TypeError):
        TypedList(0, [1, "two", 3])


def test_typed_list_append() -> None:
    """Test appending items to TypedList."""
    tlist = TypedList(0)
    tlist.append(4)
    assert tlist[0] == 4

    with pytest.raises(TypeError):
        tlist.append("not an int")


def test_typed_list_get_item() -> None:
    """Test getting items from TypedList."""
    tlist = TypedList("", ["one", "two", "three"])
    assert tlist[0] == "one"
    assert tlist[1] == "two"
    assert tlist[2] == "three"

    tlist = TypedList(0)
    with pytest.raises(IndexError):
        _ = tlist[0]


def test_typed_list_set_item() -> None:
    """Test setting items in TypedList."""
    tlist = TypedList("", ["one", "two", "three"])
    tlist[1] = "changed"
    assert tlist[1] == "changed"
    assert tlist[0] == "one"
    assert tlist[2] == "three"

    with pytest.raises(TypeError):
        tlist[0] = 123


def test_typed_list_length() -> None:
    """Test length of TypedList."""
    tlist = TypedList(0, [1, 2, 3])
    assert len(tlist) == 3

    tlist.append(4)
    assert len(tlist) == 4

    del tlist[0]
    assert len(tlist) == 3

    tlist = TypedList("example")
    assert len(tlist) == 0


def test_typed_list_deletion() -> None:
    """Test deletion of items in TypedList."""
    tlist = TypedList("", ["one", "two", "three"])
    del tlist[1]
    assert len(tlist) == 2
    assert tlist[0] == "one"
    assert tlist[1] == "three"

    with pytest.raises(IndexError):
        del tlist[5]

    tlist = TypedList(0)
    with pytest.raises(IndexError):
        del tlist[0]


def test_typed_list_concatenation() -> None:
    """Test concatenation of two TypedLists."""
    tlist1 = TypedList("", ["one", "two"])
    tlist2 = TypedList("", ["three", "four"])
    tlist3 = tlist1 + tlist2
    assert len(tlist3) == 4
    assert tlist3[0] == "one"
    assert tlist3[1] == "two"
    assert tlist3[2] == "three"
    assert tlist3[3] == "four"

    tlist_int = TypedList(0, [1, 2])
    with pytest.raises(TypeError):
        _ = tlist1 + tlist_int


def test_typed_list_repetition() -> None:
    """Test repetition of TypedList."""
    tlist = TypedList(0, [1, 2, 3])
    tlist_repeated = tlist * 3
    assert len(tlist_repeated) == 9
    assert tlist_repeated[0] == 1
    assert tlist_repeated[1] == 2
    assert tlist_repeated[2] == 3
    assert tlist_repeated[3] == 1
    assert tlist_repeated[4] == 2
    assert tlist_repeated[5] == 3
    assert tlist_repeated[6] == 1
    assert tlist_repeated[7] == 2
    assert tlist_repeated[8] == 3

    tlist_repeated_rm = 2 * tlist
    assert len(tlist_repeated_rm) == 6
    assert tlist_repeated_rm[0] == 1
    assert tlist_repeated_rm[1] == 2
    assert tlist_repeated_rm[2] == 3
    assert tlist_repeated_rm[3] == 1
    assert tlist_repeated_rm[4] == 2
    assert tlist_repeated_rm[5] == 3


def test_typed_list_iteration() -> None:
    """Test iteration over TypedList."""
    tlist = TypedList("", ["one", "two", "three"])
    items = []
    for item in tlist:
        items.append(item)  # noqa: PERF402
    assert items == ["one", "two", "three"]


def test_typed_list_unpacking() -> None:
    """Test unpacking of TypedList."""
    tlist = TypedList("", ["one", "two", "three"])
    a, b, c = tlist
    assert a == "one"
    assert b == "two"
    assert c == "three"

    with pytest.raises(ValueError):  # noqa: PT011
        a, b = tlist


def test_typed_list_type_enforcement() -> None:
    """Test that TypedList enforces type constraints."""
    tlist = TypedList(0)
    with pytest.raises(TypeError):
        tlist.append("string instead of int")

    with pytest.raises(TypeError):
        tlist[0] = "another string"


def test_typed_list_repr() -> None:
    """Test the string representation of TypedList."""
    tlist = TypedList("", ["one", "two", "three"])
    assert repr(tlist) == "TypedList(['one', 'two', 'three'])"

    tlist = TypedList(0)
    assert repr(tlist) == "TypedList([])"
