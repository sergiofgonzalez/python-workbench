"""Illustrate how to create lazy attributes using properties."""

import time


class User:
    """Represent a user in the application."""

    def __init__(self, username: str) -> None:
        """Initialize User instances."""
        self.username = username
        self.profile_data = self._get_profile_data()
        print(f"User {self.username} has been initialized")

    def _get_profile_data(self) -> str:
        print(f">>> Retrieving {self.username}'s profile data from the server")
        time.sleep(1)  # Simulate a network delay
        return f"profile data for {self.username}"


class UserV2:
    """Represent a user in the application (with lazy attributes)."""

    def __init__(self, username: str) -> None:
        """Initialize User instances."""
        self.username = username
        self._profile_data: str | None = None
        print(f"User {self.username} has been initialized")

    @property
    def profile_data(self) -> str:
        """Lazily load and return the profile data."""
        if self._profile_data is None:
            print(f">> property: Loading profile data for {self.username}")
            self._profile_data = self._get_profile_data()
        return self._profile_data

    def _get_profile_data(self) -> str:
        print(f">>> Retrieving {self.username}'s profile data from the server")
        time.sleep(1)  # Simulate a network delay
        return f"profile data for {self.username}"


def get_followers(username: str) -> list[User]:
    """Return the list of followers of the given username."""
    print(f">>> Retrieving {username}'s followers")
    followers = ["Jason", "Florence", "Margot"]
    return [User(username) for username in followers]


def get_followers_v2(username: str) -> list[UserV2]:
    """Return the list of followers of the given username."""
    print(f">>> Retrieving {username}'s followers")
    followers = ["Jason", "Florence", "Margot"]
    return [UserV2(username) for username in followers]


def eager_access() -> None:
    """Demonstrate eager access to user profile data."""
    emma = User("Emma")
    print(">>> About to retrieve Emma's followers: 1st access")
    start_t = time.perf_counter()
    _ = get_followers(emma.username)
    end_t = time.perf_counter()
    print(f">>> Retrieved {emma.username}'s followers in {end_t - start_t:.2f} seconds")
    print("=" * 30)
    print(">>> About to retrieve Emma's followers: 2nd access")
    start_t = time.perf_counter()
    _ = get_followers(emma.username)
    end_t = time.perf_counter()
    print(f">>> Retrieved {emma.username}'s followers in {end_t - start_t:.2f} seconds")
    print("=" * 30)


def lazy_access() -> None:
    """Demonstrate lazy access to user profile data."""
    emma = UserV2("Emma")
    print(">>> About to retrieve Emma's followers: 1st access")
    start_t = time.perf_counter()
    _ = get_followers_v2(emma.username)
    end_t = time.perf_counter()
    print(f">>> Retrieved {emma.username}'s followers in {end_t - start_t:.2f} seconds")
    print("=" * 30)
    print(">>> About to retrieve Emma's followers: 2nd access")
    start_t = time.perf_counter()
    _ = get_followers_v2(emma.username)
    end_t = time.perf_counter()
    print(f">>> Retrieved {emma.username}'s followers in {end_t - start_t:.2f} seconds")
    print("=" * 30)

    # Now only when the profile data is explicitly invoked the time will be spent,
    # and only once
    print("About to access Emma's profile_data:")
    start_t = time.perf_counter()
    _ = emma.profile_data
    print(f"Time to get profile_data: {time.perf_counter() - start_t:.2f} seconds")
    print("About to access Emma's profile_data: (2nd time)")
    start_t = time.perf_counter()
    _ = emma.profile_data
    print(f"Time to get profile_data: {time.perf_counter() - start_t:.2f} seconds")

    # Same thing for the followers, we will only evaluate their profile_data
    # when explicitly accessed
    followers = get_followers_v2(emma.username)
    start_t = time.perf_counter()
    for follower in followers:
        _ = follower.profile_data
    end_t = time.perf_counter()
    print(f"Time to get all followers' profile_data: {end_t - start_t:.2f} seconds")


def main() -> None:
    """Application entry point."""
    print("Demonstrating eager access:")
    eager_access()

    print("Demonstrating lazy access:")
    lazy_access()


if __name__ == "__main__":
    main()
