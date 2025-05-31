"""Illustrate how to do set operations in Python."""


def main() -> None:
    """Application entry point."""

    # Defining the sample space
    s = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9}
    a = {0, 2, 4, 6, 8}
    b = {1, 3, 5, 7, 9}
    c = {2, 3, 4, 5}
    d = {1, 6, 7}

    # A union C
    print("A union C:", a | c)
    print("A union C (using union method):", a.union(c))
    assert a | c == a.union(c)
    assert a.union(c) == {0, 2, 3, 4, 5, 6, 8}

    # A intersection B
    print("A intersection B:", a & b)
    print("A intersection B (using intersection method):", a.intersection(b))
    assert a & b == a.intersection(b)
    assert a.intersection(b) == set()

    # C complement
    c_complement = s - c
    print("C complement:", c_complement)
    print("C complement (using difference method):", s.difference(c))
    assert c_complement == s.difference(c)
    assert s.difference(c) == {0, 1, 6, 7, 8, 9}

    # (C' intersection D) union B
    print("C' intersection D:", c_complement & d)
    assert c_complement & d == c_complement.intersection(d)
    assert c_complement.intersection(d) == {1, 6, 7}

    # (s intersection C)'
    s_intersection_c_complement = s.intersection(c_complement)
    print("s intersection C complement:", s_intersection_c_complement)
    assert s_intersection_c_complement == s - c
    assert s - c == {0, 1, 6, 7, 8, 9}

    # A intercection C intersection D'
    d_complement = s - d
    print("D complement:", d_complement)
    a_intersection_c_intersection_d_complement = a & c & d_complement
    print(
        "A intersection C intersection D complement:",
        a_intersection_c_intersection_d_complement,
    )
    assert a_intersection_c_intersection_d_complement == a.intersection(c).intersection(
        d_complement,
    )
    assert a_intersection_c_intersection_d_complement == {2, 4}


if __name__ == "__main__":
    main()
