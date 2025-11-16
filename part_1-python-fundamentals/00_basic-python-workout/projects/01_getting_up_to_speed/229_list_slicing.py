"""Everything you wanted to know about slicing lists in Python."""

from functools import partial
from time import perf_counter
from timeit import timeit


def main() -> None:
    """Application entry point."""
    fruits = ["apple", "orange", "banana", "strawberry"]
    print(fruits)

    # Extract a sublist from index 1 to index 3 (not inclusive)
    assert fruits[1:3] == ["orange", "banana"]

    # Extract a sublist from the start to index 3 (not inclusive)
    assert fruits[:3] == ["apple", "orange", "banana"]

    # Extract a sublist from index 1 to the end
    assert fruits[1:] == ["orange", "banana", "strawberry"]

    # Extract a sublist from the start to the end (a copy of the list)
    fruits_copy = fruits[:]
    assert fruits_copy == ["apple", "orange", "banana", "strawberry"]
    assert fruits_copy is not fruits  # Ensure it's a new list
    fruits_copy[0] = "mango"
    fruits_copy.append("kiwi")
    print(fruits_copy)
    print(fruits)  # Original list remains unchanged

    print("=== PASSED ===")

    nums = list(range(1, 11))  # Create a list of numbers from 1 to 10
    print(nums)

    # Extract the elements from the 3rd to the 5th using stride
    assert nums[2:5:2] == [3, 5]

    # Extract the even numbers using stride and no end index
    assert nums[1::2] == [2, 4, 6, 8, 10]

    # Invert the list using a negative stride
    assert nums[::-1] == [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
    assert (
        list(reversed(nums)) == nums[::-1]
    )  # Ensure it matches the reversed() function

    print("=== PASSED ===")

    # timing reversing of a large list using slicing vs reversed()

    large_list = list(range(1_000_001))

    start = perf_counter()
    _ = large_list[::-1]
    end = perf_counter()
    print(f"Slicing took {end - start:.6f} seconds")

    start = perf_counter()
    _ = list(reversed(large_list))
    end = perf_counter()
    print(f"reversed() took {end - start:.6f} seconds")

    # Same exercise using timeit
    list_sizes = (10, 100, 1_000, 10_000, 100_000, 1_000_000)
    for size in list_sizes:
        large_list = list(range(size))
        slicing_time = timeit(
            stmt=partial(lambda lst: lst[::-1], large_list),
            number=1_000,
        )
        reversed_time = timeit(
            stmt=partial(lambda lst: list(reversed(lst)), large_list),
            number=1_000,
        )

        print(
            f"Size: {size:>8} | Slicing: {slicing_time:.6f} sec | "
            f"reversed(): {reversed_time:.6f} sec",
        )


if __name__ == "__main__":
    main()
