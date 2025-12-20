"""Illustrates that arguments are passed by reference in Python."""

import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

logger = logging.getLogger(__name__)


def func(lst: list[int], num: float, s: str) -> None:
    """Illustrate that arguments are passed by reference in Python."""
    logger.debug(
        "Before modification: %s (%#x), %f (%#x), %s (%#x)",
        lst,
        id(lst),
        num,
        id(num),
        s,
        id(s),
    )
    lst.append(42)
    num += 1.0
    s += " world"
    logger.debug(
        "After modification : %s (%#x), %f (%#x), %s (%#x)",
        lst,
        id(lst),
        num,
        id(num),
        s,
        id(s),
    )


def func2(t: tuple[int | list[int], ...]) -> None:
    """Illustrate that tuple elements cannot be modified in place."""
    logger.debug("Before modification: %s (%#x)", t, id(t))
    if isinstance(t[0], list):
        t[0].append(99)  # Modifying the list inside the tuple is allowed
    logger.debug("After modification : %s (%#x)", t, id(t))


def main() -> None:
    """Application entry point."""
    # variables in Python hold references to objects
    # they are like pointers in other languages
    # Python automatically updated references when objects are modified or reassigned
    x = 5
    print(f"Before modification: {x=}, id={id(x):#x}")
    x += 1
    print(f"After modification : {x=}, id={id(x):#x}")
    x = 7
    print(f"After reassignment : {x=}, id={id(x):#x}")
    print("=" * 40)

    s = "foo"
    print(f"Before modification: {s=}, id={id(s):#x}")
    s = s.capitalize()
    print(f"After modification : {s=}, id={id(s):#x}")
    s = "bar"
    print(f"After reassignment : {s=}, id={id(s):#x}")
    print("=" * 40)

    # Now let's confirm what happens with function arguments
    # mutable objects (like lists) can be modified in place
    # immutable objects (like numbers and strings) cannot be modified in place
    # (Python does not automatically update references for immutable objects)
    my_list = [1, 2, 3]
    my_num = 3.14
    my_str = "hello"
    logger.debug(
        "Before function call: %s (%#x), %f (%#x), %s (%#x)",
        my_list,
        id(my_list),
        my_num,
        id(my_num),
        my_str,
        id(my_str),
    )
    func(my_list, my_num, my_str)
    logger.debug(
        "After function call : %s (%#x), %f (%#x), %s (%#x)",
        my_list,
        id(my_list),
        my_num,
        id(my_num),
        my_str,
        id(my_str),
    )
    print("=" * 40)

    # Now let's see what happens with a tuple containing mutable and immutable elements
    # tuples themselves cannot be modified in place
    # but mutable elements inside them can be modified
    # In any case, the tuple reference itself remains unchanged
    my_tuple = (1, 2, 3)
    func2(my_tuple)
    logger.debug("After function call : %s (%#x)", my_tuple, id(my_tuple))
    print("=" * 40)
    my_tuple = ([1, 2, 3], 4, 5)
    func2(my_tuple)
    logger.debug("After function call : %s (%#x)", my_tuple, id(my_tuple))
    print("=" * 40)


if __name__ == "__main__":
    main()
