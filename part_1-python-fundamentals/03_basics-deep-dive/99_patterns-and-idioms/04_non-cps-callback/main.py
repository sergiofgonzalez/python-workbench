"""An example of a callback used in non-continuation passing style scenarios."""


def mult_by_2(n: float) -> float:
    """Function invoked as a callback by map."""  # noqa: D401
    print(f">>> mult_by_2 called with argument {n=}")
    return n * 2


def main() -> None:
    """Application entry point."""
    nums = list(range(11))
    double_nums = map(lambda x: x * 2, nums)  # noqa: C417
    print(f"{list(double_nums)=}")

    # with a named function
    double_nums = map(mult_by_2, nums)
    print(f"{list(double_nums)=}")


if __name__ == "__main__":
    main()
