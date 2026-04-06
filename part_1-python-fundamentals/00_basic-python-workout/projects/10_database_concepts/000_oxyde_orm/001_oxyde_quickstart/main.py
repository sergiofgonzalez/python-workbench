"""Oxyde quickstart showing basic operations when working with oxyde."""

import asyncio

from oxyde import db

from models import User


async def main() -> None:
    """Async application entry point."""
    # Connect to the db: note that you need to state the path here too
    await db.init(default="sqlite://./app.db")

    # Create a new user
    alice = await User.objects.create(
        name="Alice",
        email="alice@example.com",
        age=30,
    )
    print(f"Created user: {alice.name} (id={alice.id})")

    # Read the user back from the database
    users = await User.objects.filter(age__gte=25).all()
    print(f"Found {len(users)} user(s) aged 25 or older")

    # Update the user's age
    alice.age = 31
    await alice.save()
    print(f"Updated Alice's age to {alice.age}")

    # Delete the user
    await alice.delete()
    print("Deleted Alice")

    # Close the database connection
    await db.close()


if __name__ == "__main__":
    # start the evt loop in the current thread and schedule main() to run.
    asyncio.run(main())
