"""Illustrates that lookups in sets are constant time operations but not in lists."""

import timeit


def main() -> None:
    """Application entry point."""
    print("\n== Lookup Performance Report ==")
    print(f"{'Collection Size':<16} {'Set Lookup (s)':<16} {'List Lookup (s)':<16}")
    for collection_size in (10, 100, 1_000, 10_000, 100_000):
        set_setup_code_str = (
            f"from random import randint\nmy_set = set(range({collection_size}))"
        )
        list_setup_code_str = (
            f"from random import randint\nmy_list = list(range({collection_size}))"
        )
        set_stmt_check_str = (
            f"rand_val = randint(0, {collection_size - 1})\nfound = rand_val in my_set"
        )
        list_stmt_check_str = (
            f"rand_val = randint(0, {collection_size - 1})\nfound = rand_val in my_list"
        )
        t_set = timeit.timeit(
            stmt=set_stmt_check_str,
            setup=set_setup_code_str,
            number=10_000,
        )
        t_list = timeit.timeit(
            stmt=list_stmt_check_str,
            setup=list_setup_code_str,
            number=10_000,
        )

        print(f"{collection_size:>15,} {t_set:>15.6f} {t_list:>16.6f}")


if __name__ == "__main__":
    main()
