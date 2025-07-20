"""Illustrate the use of `any()` and `all()` functions."""


def main() -> None:
    """Application entry point."""
    # basic behavior of any() and all()
    print("Using any() and all() functions:")
    values = [True, False, True]
    print(f"{values=} {any(values)=}")
    print(f"{values=} {all(values)=}")

    print("===========================")
    values = [True, True, True]
    print(f"{values=} {any(values)=}")
    print(f"{values=} {all(values)=}")

    print("===========================")
    numbers = [1, 2, 3, 4, 5]

    # Check if any number is even
    if any(n % 2 == 0 for n in numbers):
        print("There is at least one even number.")
    else:
        print("There are no even numbers.")

    # Check if all numbers are even
    if all(n % 2 == 0 for n in numbers):
        print("All numbers are even.")
    else:
        print("Not all numbers are even.")


if __name__ == "__main__":
    main()
