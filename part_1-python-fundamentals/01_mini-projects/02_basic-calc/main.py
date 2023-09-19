from typing import Tuple


def print_options():
    print()
    print("A. Addition")
    print("B. Subtraction")
    print("C. Multiplication")
    print("D. Division")
    print("E. Exit")


def int_input(msg: str) -> int | None:
    """Reads an integer from the standard input

    Parameters
    ----------
    msg : str
    The prompt message

    Returns
    -------
    int | None
    the integer the user typed or None if what the user typed could not be
    parsed as an integer
    """
    s = input(f"{msg} ")
    try:
        return int(s)
    except Exception:
        print(f"Operand must be an integer, but was {s}")
        return None


def get_operands() -> Tuple[int | None, int | None]:
    n1 = int_input("Enter the first operand:")
    if not n1:
        return None, None
    n2 = int_input("Enter the second operand:")
    if not n2:
        return n1, None
    return n1, n2


print("Welcome to the Basic Calculator")
print_options()

while True:
    print()
    op = input("Choose operation: ")
    if op.lower() == "a":
        n1, n2 = get_operands()
        if not n1 or not n2:
            continue
        sum = n1 + n2
        print(f"{n1} + {n2} = {sum}")
    elif op.lower() == "b":
        n1, n2 = get_operands()
        if not n1 or not n2:
            continue
        sub = n1 - n2
        print(f"{n1} - {n2} = {sub}")
    elif op.lower() == "c":
        n1, n2 = get_operands()
        if not n1 or not n2:
            continue
        prod = n1 * n2
        print(f"{n1} * {n2} = {prod}")
    elif op.lower() == "d":
        n1, n2 = get_operands()
        if not n1 or not n2:
            continue
        division = n1 // n2
        remainder = n1 % n2
        print(f"{n1} / {n2} = {division}; remainder={remainder}")
    elif op.lower() == "e":
        print("Exiting")
        break
    else:
        print("Unknown option")
        print_options()
