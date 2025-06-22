"""Illustrate the use of static properties."""


class MyClass:
    """A class with static properties."""

    class_name: str = "MyClass"
    num_instances: int = 0

    def __init__(self) -> None:
        """Initialize the class and increment instance count."""
        MyClass.num_instances += 1


def main() -> None:
    """Application entry point."""
    print(f"Class Name: {MyClass.class_name}")
    print(f"Number of Instances: {MyClass.num_instances}")

    # Create instances
    instance1 = MyClass()
    instance2 = MyClass()

    print(f"Number of Instances after creating two instances: {MyClass.num_instances}")

    # Accessing class property
    print(f"Accessing class property: {instance1.class_name}")
    print(f"Accessing class property: {instance2.class_name}")


if __name__ == "__main__":
    main()
