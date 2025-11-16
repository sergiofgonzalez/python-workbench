"""Illustrating the kwargs dictionary."""

from typing import Any


def my_function(pos_arg0: int, pos_arg1: str, **kwargs: Any) -> None:  # noqa: ANN401
    """Take two positional arguments and any number of keyword arguments."""
    print(f"Positional arg 0 (int): {pos_arg0}")
    print(f"Positional arg 1 (str): {pos_arg1}")
    print("Keyword args (misc types):")
    print(
        "\tkwarg0: "
        f"{kwargs.get('kwarg0')} (type: {type(kwargs.get('kwarg0')).__name__})",
    )
    print(
        "\tkwarg1: "
        f"{kwargs.get('kwarg1')} (type: {type(kwargs.get('kwarg1')).__name__})",
    )
    print(
        "\tkwarg2: "
        f"{kwargs.get('kwarg2')} (type: {type(kwargs.get('kwarg2')).__name__})",
    )
    if len(kwargs) > 3:  # noqa: PLR2004
        print("\t... and more!")
        for key, value in kwargs.items():
            if key not in {"kwarg0", "kwarg1", "kwarg2"}:
                print(f"\t{key}: {value} (type: {type(value).__name__})")
    print("-" * 40)


def main() -> None:
    """Application entry point."""
    # positional arguments always have to come first and be there
    try:
        my_function(1)  # type: ignore  # noqa: PGH003
    except TypeError as err:
        print("Error calling my_function with missing positional args:", err)

    # you can switch the order of positional args using names
    my_function(pos_arg1="hello", pos_arg0=42)

    # calling with only positional args in the expected order
    my_function(1, "a")

    # calling with positional and keyword args
    my_function(2, "a", kwarg0=5)

    # calling with more keyword args
    my_function(3, "a", kwarg0=5, kwarg2="red")

    # You can direcly pass a dict as kwargs using the ** unpacking operator
    kwargs_dict = {
        "kwarg0": 5,
        "kwarg2": "red",
    }
    my_function(4, "a", **kwargs_dict)

    # you can pass many more keyword args than expected
    kwargs_dict = {
        "kwarg0": 5,
        "kwarg1": [1, 2, 3],
        "kwarg2": "red",
        "kwarg3": (4, 5),
        "kwarg4": {"a": 1, "b": 2},
    }
    my_function(4, "a", **kwargs_dict)


if __name__ == "__main__":
    main()
