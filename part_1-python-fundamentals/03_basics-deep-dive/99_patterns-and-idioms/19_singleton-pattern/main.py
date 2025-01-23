"""Using the Singleton pattern."""

from db_instance import Database
from module_a import get_db_instance as get_db_instance_from_a
from module_b import get_db_instance as get_db_instance_from_b


def main() -> None:
    """Application entry-point."""
    is_same_instance = get_db_instance_from_a() is get_db_instance_from_b()
    print(f"{is_same_instance=}")

    # instantiate another instance with the same details
    some_other_instance = Database("my_db", "my_connection_details")
    is_same_instance = get_db_instance_from_a() is some_other_instance
    print(f"{is_same_instance=}")


if __name__ == "__main__":
    main()
