"""Illustrate how to serialize legacy namedtuples into JSON."""

import json
from collections import namedtuple


class Wrapper:
    """A wrapper class to serialize NamedTuples."""

    def __init__(self, nt: namedtuple) -> None:  # type: ignore  # noqa: PGH003, PYI024
        """Initialize the Wrapper instance."""
        self.nt = nt


def main() -> None:
    """Application entry point."""
    Task = namedtuple("Task", ["title", "description", "urgency"])  # noqa: PYI024
    task = Task("Homework", "Physics and math", 5)

    # Default JSON output is not probably what you want
    json_str1 = json.dumps(task)
    print(f"{json_str1=}")

    # We can serialize it with a default function, but __dict__ won't give you
    # the expected results either
    json_str2 = json.dumps(task, default=lambda t: t.__dict__)
    print(f"{json_str2=}")

    # The best way is to convert it to a dictionary manually
    json_str3 = json.dumps(
        {
            "title": task.title,
            "description": task.description,
            "urgency": task.urgency,
        },
    )
    print(f"{json_str3=}")

    # Using a custom serialization function won't work, because
    # the encoder function is not called for NamedTuples by default
    def serialize_namedtuple(obj: Task) -> dict:
        if isinstance(obj, Task):  # type: ignore  # noqa: PGH003
            return {
                "title": obj.title,
                "description": obj.description,
                "urgency": obj.urgency,
            }
        msg = f"Type {type(obj)} not serializable"
        raise TypeError(msg)

    json_str4 = json.dumps(task, default=serialize_namedtuple)
    print(f"{json_str4=}")

    # Another solution is to use a wrapper class, then the default function
    # will be called
    def custom_encoder(o: Wrapper) -> dict:
        return {
            "title": o.nt.title,
            "description": o.nt.description,
            "urgency": o.nt.urgency,
        }

    wrapper = Wrapper(task)
    json_str5 = json.dumps(wrapper, default=custom_encoder)
    print(f"{json_str5=}")


if __name__ == "__main__":
    main()
