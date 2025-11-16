"""Illustrate the use of .setdefault() method in dictionaries."""


def main() -> None:
    """Application entry point."""
    tasks = {
        "laundry": 3,
        "homework": 5,
        "museum": 2,
    }
    print(f"Before: {tasks=}")
    print(f"{tasks.setdefault("laundry", 0)=}")
    print(f"{tasks.setdefault("go to the gym", 0)=}")
    print(f"After: {tasks=}")


if __name__ == "__main__":
    main()
