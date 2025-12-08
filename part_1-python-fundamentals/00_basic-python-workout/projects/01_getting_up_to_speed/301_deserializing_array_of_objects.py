"""A practical example showing how to deserialize an array of JSON objects."""

import json


def main() -> None:
    """Application entry point."""
    json_string = """
    [
        {
            "title": "Laundry",
            "desc": "Wash clothes",
            "urgency": 3
        },
        {
            "title": "Homework",
            "desc": "Physics + Math",
            "urgency": 5
        }
    ]
    """
    # Plain deserialization does not produce the expected results
    python_list_of_objs = json.loads(json_string)
    print(python_list_of_objs)

    # We can iterate over the list of deserialized objects: they are dicts
    for item in json.loads(json_string):
        print(f"Item: {item}, Type: {type(item).__name__}")


if __name__ == "__main__":
    main()
