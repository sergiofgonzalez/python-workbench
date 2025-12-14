"""Illustrate the difference between shallow and deep copy."""

import copy


def print_val_and_id(val: object, label: str) -> None:
    """Print the value and id of a variable.

    Args:
        val: The variable whose value and id to print.
        label: The label of the variable.

    """
    print(f"{label}: value={val}, id={id(val):#x}")


def main() -> None:  # noqa: PLR0915
    """Application entry point."""
    # Multiple ways of doing a shallow copy of a list
    original = [[1, 2], 3]
    shallow_copy_1 = list(original)
    shallow_copy_2 = original[:]
    shallow_copy_3 = original.copy()
    shallow_copy_4 = original + []  # noqa: RUF005
    shallow_copy_5 = original * 1
    shallow_copy_6 = [item for item in original]  # noqa: C416
    shallow_copy_7 = [*original]

    # Probably, the clearest way is original[:]
    assert shallow_copy_1 == original
    assert shallow_copy_2 == original
    assert shallow_copy_3 == original
    assert shallow_copy_4 == original
    assert shallow_copy_5 == original
    assert shallow_copy_6 == original
    assert shallow_copy_7 == original

    # Let's validate these are shallow copies
    # (i.e., all the copies are linked and pointing to the same nested objects)
    original[0][0] = 99
    print(f"After modifying original, shallow_copy_1: {shallow_copy_1}")  # [[99, 2], 3]
    print(f"After modifying original, shallow_copy_2: {shallow_copy_2}")  # [[99, 2], 3]
    print(f"After modifying original, shallow_copy_3: {shallow_copy_3}")  # [[99, 2], 3]
    print(f"After modifying original, shallow_copy_4: {shallow_copy_4}")  # [[99, 2], 3]
    print(f"After modifying original, shallow_copy_5: {shallow_copy_5}")  # [[99, 2], 3]
    print(f"After modifying original, shallow_copy_6: {shallow_copy_6}")  # [[99, 2], 3]
    print(f"After modifying original, shallow_copy_7: {shallow_copy_7}")  # [[99, 2], 3]

    shallow_copy_2[0][1] = 88
    print(f"After modifying shallow_copy_2, original: {original}")  # [[
    print(f"After modifying original, shallow_copy_2: {shallow_copy_2}")  # [[99, 2], 3]
    print(f"After modifying original, shallow_copy_3: {shallow_copy_3}")  # [[99, 2], 3]
    print(f"After modifying original, shallow_copy_4: {shallow_copy_4}")  # [[99, 2], 3]
    print(f"After modifying original, shallow_copy_5: {shallow_copy_5}")  # [[99, 2], 3]
    print(f"After modifying original, shallow_copy_6: {shallow_copy_6}")  # [[99, 2], 3]
    print(f"After modifying original, shallow_copy_7: {shallow_copy_7}")  # [[99, 2], 3]
    print("=" * 40)

    # Now let's do a deep copy
    # (i.e., the copy is independent and not linked to the original)
    deep_copy = copy.deepcopy(original)
    print(f"original before modifying deep_copy: {original}")  # [[99, 88], 3]
    print(f"deep_copy before modifying deep_copy: {deep_copy}")  # [[99
    deep_copy[0][0] = 77
    print(f"original after modifying deep_copy: {original}")  # [[99, 88], 3]
    print(f"deep_copy after modifying deep_copy: {deep_copy}")  # [[77, 88], 3]
    print("=" * 40)

    # Now the exercise
    original = [[0], 1]
    shallow = original[:]
    # original and shadow point to different list objects
    print_val_and_id(original, "original")
    print_val_and_id(shallow, "shallow ")
    # but their first elements point to the same nested list object
    print_val_and_id(original[0], "original[0]")
    print_val_and_id(shallow[0], "shallow[0] ")
    print("-" * 40)

    # Now we create a deep copy
    deep = copy.deepcopy(original)
    print_val_and_id(original, "original")
    print_val_and_id(deep, "deep    ")
    # and their first elements point to different nested list objects
    print_val_and_id(original[0], "original[0]")
    print_val_and_id(deep[0], "deep[0]    ")
    print("-" * 40)

    # If we modify the shallow copy, the original is affected
    # but not the deep copy
    shallow[0][0] = 55
    print("After modifying shallow[0][0]:")
    print(f"original: {original}")  # [[55], 1]
    print(f"shallow:  {shallow}")  # [[55], 1]
    print(f"deep:     {deep}")  # [[0], 1]
    print("-" * 40)

    # if we modify the deep copy, the original is not affected
    deep[0][0] = 99
    print("After modifying deep[0][0]:")
    print(f"original: {original}")  # [[55], 1]
    print(f"shallow:  {shallow}")  # [[55], 1
    print(f"deep:     {deep}")  # [[99], 1]
    print("-" * 40)

    # Last point
    x = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    y = copy.deepcopy(x)

    for v in y:
        # We cannot iterate and modify the list directly because
        # we would be creating a new local variable v that would
        for i in range(len(v)):
            v[i] *= 10

    print(f"x: {x}")  # [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    print(f"y: {y}")  # [[10, 20, 30], [40, 50, 60], [70, 80, 90]]


if __name__ == "__main__":
    main()
