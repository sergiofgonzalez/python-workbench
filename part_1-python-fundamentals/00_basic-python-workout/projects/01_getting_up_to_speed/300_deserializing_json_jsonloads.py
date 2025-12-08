"""Illustrates the basics of JSON deserialization/unmarshalling using json.loads."""

import json


def print_value_and_type(value: object) -> None:
    """Print the value and its type."""
    if isinstance(value, str):
        print(f"Value: {value!r}, Type: {type(value).__name__}")
    else:
        print(f"Value: {value}, Type: {type(value).__name__}")


def main() -> None:
    """Application entry point."""
    json_strings_by_json_type = {
        "String": '"one"',
        "Number (1)": "42",
        "Number (2)": "3.14",
        "Boolean (true)": "true",
        "Boolean (false)": "false",
        "Array": '[1, 2, "blue"]',
        "Object": '{"name": "Alice", "age": 30}',
        "Null": "null",
    }

    for json_type, json_string in json_strings_by_json_type.items():
        deserialized_value = json.loads(json_string)
        print(f"JSON Type: {json_type} | JSON value: {json_string}", end=" => ")
        print_value_and_type(deserialized_value)

    print("=" * 40)

    # You have to be strict with JSON syntax!
    invalid_json_strings = [
        "{name: 'Alice', age: 30}",  # Keys must be double-quoted strings
        "['one', 'two', 'three']",   # Strings must be double-quoted
        "True",                      # Must be lowercase 'true'
        "None",                      # Must be 'null'
        "undefined",                 # Not a valid JSON value
    ]

    for invalid_json in invalid_json_strings:
        try:
            json.loads(invalid_json)
        except json.JSONDecodeError as e:
            print(f"Invalid JSON: {invalid_json!r} => Error: {e}")




if __name__ == "__main__":
    main()
