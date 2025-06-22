"""Illustrate how to define read-only/write only attributes in Python using @property."""


class User:
    """A class with read-only attributes using @property."""

    def __init__(self, username: str, password: str) -> None:
        """Initialize the user with a username and password."""
        self._username = username
        self._password = password

    @property
    def username(self) -> str:
        """Get the username of the user."""
        return self._username  # Read-only attribute

    # password is a write-only attribute
    @property
    def password(self) -> None:
        """Get the password of the user."""
        msg = "Password is a write-only attribute"
        raise AttributeError(msg)

    @password.setter
    def password(self, value: str) -> None:
        """Set the password of the user."""
        if len(value) < 8:  # noqa: PLR2004
            msg = "Password must be at least 8 characters long"
            raise ValueError(msg)
        self._password = value

    def __repr__(self) -> str:
        """Return a string representation of the user."""
        return f"User(username={self._username}, password=******)"


def main() -> None:
    """Application entry point."""
    user = User("john_doe", "securepassword123")
    print(user)  # Output: User(username=john_doe, password=******)
    print(f"Username: {user.username}")  # Output: Username: john_doe
    try:
        print(
            user.password,
        )  # This will raise an AttributeError since password is write-only
    except AttributeError as e:
        print(f"Error: {e}")
    user.password = "new_secure_password"  # Set a new password  # noqa: S105


if __name__ == "__main__":
    main()
