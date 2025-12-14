"""Practical example of string split and join operations."""


def main() -> None:
    """Application entry point."""
    s = "This is a test"
    s_words = s.split()  # Split the string into words
    s_dashes = "-".join(s_words)  # Join the words with dashes
    assert s == "This is a test"
    assert s_dashes == "This-is-a-test"
    assert s_dashes == s.replace(" ", "-")
    print("=== all asserts passed ===")


if __name__ == "__main__":
    main()
