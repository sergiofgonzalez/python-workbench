"""Illustrates how to serialize Python objects into JSON using json.dumps."""

import json


def main() -> None:
    """Application entry point."""
    lst = ["one", True, {"0": None, 1: [1.0, 2.0]}]
    json_str = json.dumps(lst)
    print(f"{json_str=}, type={type(json_str).__name__}")


if __name__ == "__main__":
    main()
