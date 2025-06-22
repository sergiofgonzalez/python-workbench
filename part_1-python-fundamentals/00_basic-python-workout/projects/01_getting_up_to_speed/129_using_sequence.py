"""Illustrate the Sequence type to annotate iterables."""

from collections.abc import Sequence


def print_sequence_elements(seq: Sequence[int | str]) -> None:
    """Print each element in the sequence."""
    for index, element in enumerate(seq):
        print(f"Element {index}: {element}")


def main() -> None:
    """Application entry point."""
    my_sequence: Sequence[int] = [1, 2, 3, 4, 5]
    print_sequence_elements(my_sequence)  # Should print each element in the sequence
    my_tuple: Sequence[str] = ("apple", "banana", "cherry")
    print_sequence_elements(my_tuple)  # Should print each element in the tuple

    # While sets and dicts are not Sequence, it still works!
    my_set = {10, 20, 30}
    print_sequence_elements(my_set) # type: ignore  # noqa: PGH003

    my_dict = {"key1": "value1", "key2": "value2"}
    print_sequence_elements(my_dict)  # type: ignore  # noqa: PGH003


if __name__ == "__main__":
    main()
