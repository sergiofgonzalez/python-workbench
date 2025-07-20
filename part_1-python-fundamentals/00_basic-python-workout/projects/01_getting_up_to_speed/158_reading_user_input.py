"""Basic internal vault with username/password authentication and lockout."""

import getpass


def main() -> None:
    """Application entry point."""
    # Internal vault with usernames and passwords
    vault = {
        "admin": "secret123",
        "user1": "password456",
        "alice": "wonderland",
        "bob": "builder",
        "charlie": "chocolate",
    }

    max_attempts = 3
    current_attempts = 0

    print("Welcome to the Internal Vault System")
    print("=" * 40)

    while current_attempts < max_attempts:
        print(f"\nAttempt {current_attempts + 1} of {max_attempts}")

        # Get username and password from user
        username = input("Username: ").strip()
        password = getpass.getpass("Password: ")  # Hides password input

        # Check credentials
        if username in vault and vault[username] == password:
            print(f"\n✅ Welcome, {username}! Access granted.")
            print("You have successfully logged into the vault.")
            return

        current_attempts += 1
        remaining = max_attempts - current_attempts

        if remaining > 0:
            print(f"❌ Invalid credentials. {remaining} attempt(s) remaining.")
        else:
            print("❌ Invalid credentials.")

    # Max attempts reached
    print("\n🔒 ACCOUNT LOCKED!")
    print("Maximum number of login attempts exceeded.")
    print("Please contact the administrator to unlock your account.")


if __name__ == "__main__":
    main()
