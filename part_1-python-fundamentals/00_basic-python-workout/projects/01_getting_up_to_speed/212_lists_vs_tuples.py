"""Illustrate the basic differences between lists and tuples."""


def main() -> None:
    """Application entry point."""
    # Create a list with the numbers 0, 1, 2, 3
    my_list = [0, 1, 2, 3]
    print("List:", my_list)

    # Insert the number -1 at the head of the list
    my_list.insert(0, -1)
    print("List after insert:", my_list)

    # Insert the number 4 at the tail of the list
    my_list.append(4)
    print("List after append:", my_list)

    # Extend the list with another list with the numbers 5, 6, 7
    my_list.extend([5, 6, 7])
    print("List after extend:", my_list)

    # Trying to remove the element 8 from the list
    try:
        my_list.remove(8)
    except ValueError as err:
        print("Error trying to remove 8 from list:", err)

    # Trying to remove the element 5 from the list
    my_list.remove(5)
    print("List after removing 5:", my_list)

    # Remove the element in the 5th index
    removed_element = my_list.pop(5)
    print("Removed element at index 5:", removed_element)
    print("List after popping index 5:", my_list)

    print("-" * 80)
    # Create a tuple with the numbers 1, 2, 3
    my_tuple = (1, 2, 3)
    print("Tuple:", my_tuple)

    # Try to change the first element of the tuple to 2
    try:
        my_tuple[0] = 2  # type: ignore  # noqa: PGH003
    except TypeError as err:
        print("Error trying to change the first element of the tuple:", err)

    # Create a tuple with the elements 1, 2, 3 and b, c
    another_tuple = (1, 2, 3, "b", "c")
    print("Another Tuple:", another_tuple)

    # Create a tuple from the lists [1, 2, 3] and ['b', 'c']
    list1 = [1, 2, 3]
    list2 = ["b", "c"]
    combined_tuple = (*list1, *list2)
    print("Combined Tuple:", combined_tuple)

    # Create a tuple having the elements [1, 2, 3] and ['b', 'c'] as elements
    nested_tuple = (list1, list2)
    print(f"Nested Tuple: {nested_tuple} (0x{id(nested_tuple):x})")

    # Updating the first element of the list inside the nested tuple
    # to append the number 4 and the second element to prepend "a" (as first element)
    nested_tuple[0].append(4)
    nested_tuple[1].insert(0, "a")
    print(
        f"Nested Tuple after modifying the lists inside: {nested_tuple} (0x{id(nested_tuple):x})"
    )

    # Understanding why it let us modify the lists inside the tuple
    # in terms of hexadecimal ids
    # See how the id of the tuple is the same, and the ids of the lists inside
    # are the same as the original lists, meaning they are the same objects
    # so immutability of the tuple is preserved
    print(f"Id of the tuple: 0x{id(nested_tuple):x}")
    print(f"Id of the first list inside the nested tuple: 0x{id(nested_tuple[0]):x}")
    print(f"Id of the second list inside the nested tuple: 0x{id(nested_tuple[1]):x}")
    print(f"Id of list1: 0x{id(list1):x}")
    print(f"Id of list2: 0x{id(list2):x}")


if __name__ == "__main__":
    main()
