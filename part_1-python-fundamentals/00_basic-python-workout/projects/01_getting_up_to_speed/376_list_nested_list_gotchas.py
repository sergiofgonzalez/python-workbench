"""Nested lists gotchas (related to variables being labels in Python)."""


def print_val_and_id(val: object, label: str) -> None:
    """Print the value and id of a variable.

    Args:
        val: The variable whose value and id to print.
        label: The label of the variable.

    """
    print(f"{label}: value={val}, id={id(val):#x}")


def main() -> None:
    """Application entry point."""
    x = [0]
    y = [x, 1]
    print(f"Initial y: {y}")  # [[0], 1]
    print_val_and_id(x, "x   ")
    print_val_and_id(y[0], "y[0]")
    initial_id_x = id(x)
    print("=" * 40)

    # The nested list can be modified using x or y
    # (they are pointing to the same object in memory)
    x[0] = 55
    print(f"After modifying x, y: {y}")  # [[55], 1]
    print(f"After modifying x, x: {x}")  # [55]
    y[0][0] = 9
    print(f"After modifying y, y: {y}")  # [[9], 1]
    print(f"After modifying y, x: {x}")  # [9]
    print("=" * 40)

    # Reassigning x breaks the link between x and y[0]
    # (They no longer point to the same object in memory)
    x = [5]
    print(f"After modifying x, y: {y}")  # [[9], 1]
    print(f"After modifying x, x: {x}")  # [5]
    print_val_and_id(x, "x   ")
    print_val_and_id(y[0], "y[0]")
    print("initial id(x):     ", f"{initial_id_x:#x}")
    print("=" * 40)


if __name__ == "__main__":
    main()
