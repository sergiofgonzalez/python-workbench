"""Exiting your CLI app."""

import typer

existing_usernames = ["rick", "morty"]


def maybe_create_user(username: str) -> None:
    """Try to create username."""
    if username in existing_usernames:
        print("The user already exists.")
        raise typer.Exit(code=1)
    if username == "root":
        print("root user is reserved.")
        raise typer.Abort
    print(f"User {username} has been created.")


def send_new_user_notification(username: str) -> None:
    """Send notification to the new user."""
    print(f"Notification sent to new user: {username}")


def main(username: str) -> None:
    """CLI app entry point."""
    maybe_create_user(username)
    send_new_user_notification(username)


if __name__ == "__main__":
    typer.run(main)
