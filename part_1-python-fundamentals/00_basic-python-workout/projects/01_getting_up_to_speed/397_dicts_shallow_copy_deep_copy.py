"""Illustrates shallow copy and deep copy of dictionaries."""

import copy


def main() -> None:
    """Application entry point."""
    # dict with immutable values
    d = {"a": 1, "b": 2, "c": 3}
    shallow_copy_d = d.copy()
    deep_copy_d = copy.deepcopy(d)  # same as shallow copy for immutable values
    print(f"Original dict: {d}")
    print(f"Shallow copy dict: {shallow_copy_d}")
    print(f"Deep copy dict: {deep_copy_d}")
    print("=" * 40)

    d["a"] = 10
    print("After modifying original dict:")
    print(f"Original dict: {d}")
    print(f"Shallow copy dict: {shallow_copy_d}")
    print(f"Deep copy dict: {deep_copy_d}")
    print("=" * 40)

    # dict with mutable values
    d = {"a": [1, 2], "b": [3, 4], "c": [5, 6]}
    shallow_copy_d = d.copy()
    deep_copy_d = copy.deepcopy(d)  # different from shallow copy for mutable values
    print(f"Original dict: {d}")
    print(f"Shallow copy dict: {shallow_copy_d}")
    print(f"Deep copy dict: {deep_copy_d}")
    print("=" * 40)

    d["a"].append(10)
    print("After modifying original dict:")
    print(f"Original dict: {d}")
    print(f"Shallow copy dict: {shallow_copy_d}")
    print(f"Deep copy dict: {deep_copy_d}")
    print("=" * 40)


if __name__ == "__main__":
    main()
