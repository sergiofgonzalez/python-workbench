"""Illustrates how to create a dict dynamically with a generator."""


def main() -> None:
    """Application entry point."""
    str_to_check = "Jason Isaacs"
    freq_map = {}
    for char in str_to_check.lower():
        if char in freq_map:
            freq_map[char] += 1
        else:
            freq_map[char] = 1
    print(freq_map)

    # There are more pythonic ways to do this using a generator expression
    freq_map_gen = {
        char: str_to_check.lower().count(char) for char in str_to_check.lower()
    }
    print(freq_map_gen)


if __name__ == "__main__":
    main()
