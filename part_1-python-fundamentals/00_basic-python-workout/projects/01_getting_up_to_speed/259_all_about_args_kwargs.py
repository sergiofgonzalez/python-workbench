"""Practical examples of args, kwargs, *, and /."""

from typing import Any


def stringify(*args: Any) -> list[str]:  # noqa: ANN401
    """Convert all arguments to strings."""
    for i, arg in enumerate(args):
        print(f"args[{i}]: {arg}")
    print("===")

    return [str(arg) for arg in args]


def stringify_a(item0: int, *items: Any) -> list[str]:  # noqa: ANN401
    """Convert all arguments to strings."""
    print(f"item0: {item0}")
    for i, item in enumerate(items):
        print(f"items[{i}]: {item}")
    print("===")

    return [str(item0)] + [str(item) for item in items]


def stringify_b(*items: int, item: int) -> list[str]:
    """Convert all arguments to strings."""
    for i, val in enumerate(items):
        print(f"items[{i}]: {val}")
    print(f"item (keyword arg): {item}")
    print("===")

    return [str(val) for val in items] + [str(item)]


def print_student_report(name: str, **grades: float) -> None:
    """Print a simple grades report for the student."""
    print(f">>> DEBUG: got {grades} ({type(grades).__name__}) for {name}")
    print(f"***** Report Begin for {name} *****")
    for subject, grade in grades.items():
        print(f"### {subject + ':':5} {grade:>3}")
    print(f"***** Report End for {name}   *****")


def example(*, item1: str, item2: str, item3: str) -> None:
    """Allow only keyword args."""
    print(f"item1 (keyword): {item1}")
    print(f"item2 (keyword): {item2}")
    print(f"item3 (keyword): {item3}")


def example2(item1: str, item2: str, item3: str, /) -> None:
    """Allow only positional args."""
    print(f"item1 (positional): {item1}")
    print(f"item2 (positional): {item2}")
    print(f"item3 (positional): {item3}")


def example3(pos0: str, /, *args: str, kw: str) -> None:
    """Specific signature."""
    print(f"pos0 (positional-only): {pos0}")
    if len(args) == 0:
        print("No args")
    for i, arg in enumerate(args):
        print(f"args[{i}] (pos-only): {arg}")
    print(f"kw (keyword): {kw}")
    print("===")


def example4(pos_0: str, pos_1: str, /, kw_or_pos: str, *, kw_only: str) -> None:
    """Specific signature for the exercise."""
    print(f"pos_0 (pos only): {pos_0}")
    print(f"pos_1 (pos only): {pos_1}")
    print(f"kw_or_pos (pos/kw): {kw_or_pos}")
    print(f"kw_only: {kw_only}")
    print("===")


def main() -> None:
    """Application entry point."""
    # exercise 1
    stringify(1, (1, "two"))
    stringify(1, "two", None)
    print("=" * 40)

    # exercise 2
    stringify_a(0)
    stringify_a(0, 1)
    stringify_a(0, 1, 2)
    stringify_a(0, *[1, 2])
    print("=" * 40)

    # exercise 3
    try:
        # can't be invoked with positional-only params (item keyword is required)
        stringify_b(0)  # type: ignore  # noqa: PGH003
    except TypeError as e:
        print(f"Error: {e}")

    try:
        # can't be invoked with positional-only params (item keyword is required)
        stringify_b(0, 1)  # type: ignore  # noqa: PGH003
    except TypeError as e:
        print(f"Error: {e}")

    stringify_b(0, item=1)
    stringify_b(0, 1, 2, item=3)
    print("=" * 40)

    # exercise 4
    print_student_report("John", math=100, phys=98, bio=95)
    print("=" * 40)

    # exercise 5
    example(item1="Hello", item2="to", item3="Jason")
    try:
        example("Hello", "to", "Jason")  # type: ignore  # noqa: PGH003
    except TypeError as e:
        print(f"Error: {e}")
    print("=" * 40)

    # exercise 6
    example2("Hello", "to", "Jason")
    try:
        example2(item1="Hello", item2="to", item3="Jason")  # type: ignore  # noqa: PGH003
    except TypeError as e:
        print(f"Error: {e}")
    print("=" * 40)

    # exercise 7
    example3("positional_0", kw="last_kw")
    try:
        example3(pos0="positional_0", kw="last")  # type: ignore  # noqa: PGH003
    except TypeError as e:
        print(f"Error: {e}")
    print("===")
    example3("positional_0", "positional_1", "positional_2", kw="last_kw")

    # exercise 8
    example4("item0", "item1", kw_or_pos="item2", kw_only="item3")
    example4("item0", "item1", "item2", kw_only="item3")
    try:
        example4(pos_0="item0", pos_1="item1", kw_or_pos="item2", kw_only="item3")  # type: ignore  # noqa: PGH003
    except TypeError as e:
        print(f"Error: {e}")
    print("===")


if __name__ == "__main__":
    main()
