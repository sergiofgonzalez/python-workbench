"""Differences between type() and isinstance() with class hierarchies."""


class User:
    """Represent a user in a system."""


class Supervisor(User):
    """Represent a supervisor, which is a type of user."""


def main() -> None:
    """Application entry point."""
    supervisor = Supervisor()

    # assertions first
    assert type(supervisor) is Supervisor
    assert type(supervisor) is not User
    assert isinstance(supervisor, User)
    assert isinstance(supervisor, Supervisor)

    # now the report
    print(f"type(supervisor) is User: {type(supervisor) is User}")
    print(f"type(supervisor) is Supervisor: {type(supervisor) is Supervisor}")
    print(f"isinstance(supervisor, User): {isinstance(supervisor, User)}")
    print(f"isinstance(supervisor, Supervisor): {isinstance(supervisor, Supervisor)}")


if __name__ == "__main__":
    main()
