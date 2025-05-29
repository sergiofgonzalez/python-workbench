"""Illustrate how to do unpacking and slicing in Python."""


def main() -> None:
    """Application entry point."""
    friends = ["jane", "john", "jill", "jack"]
    jack = friends[-1]
    assert jack == "jack"
    print(f"Jack is the last friend: {jack}")

    rest_of_friends = friends[:-1]
    assert rest_of_friends == ["jane", "john", "jill"]
    print(f"Rest of friends: {rest_of_friends}")


if __name__ == "__main__":
    main()
