"""Illustrate a few scenarios where comprehensions are not recommended."""


def main() -> None:
    """Application entry point."""
    # 1. When you're not manipulating individual elements, and are just
    # transforming one type of iterable into another type of iterable.
    nums = [1, 2, 4, 2, 4, 5, 1, 2, 3, 4]

    # Using a set comprehension is cumbersome
    nums_set = {num for num in nums}  # noqa: C416
    assert nums_set == {1, 2, 3, 4, 5}

    # Using set is cleaner and more concise
    nums_set = set(nums)
    assert nums_set == {1, 2, 3, 4, 5}

    # 2. If the expression in the comprehension is too complex it is better
    # to use other approaches

    styles = ["long-sleeve", "v-neck"]
    colors = ["white", "black"]
    sizes = ["L", "S"]

    # creating all possible combos with list comprehension
    combos = [
        " ".join([style, color, size])  # noqa: FLY002
        for style in styles
        for color in colors
        for size in sizes
    ]
    print(combos)

    # Ruff recommends using an f-string
    combos = [
        f"{style} {color} {size}"
        for style in styles
        for color in colors
        for size in sizes
    ]
    print(combos)

    # In any case, using nested loops feels easier to understand
    combos = []
    for style in styles:
        for color in colors:
            for size in sizes:
                combos.append(f"{style} {color} {size}")
    print(combos)


if __name__ == "__main__":
    main()
