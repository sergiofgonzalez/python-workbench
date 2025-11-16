"""Illustrates how to create lazy attributes using __getattr__."""

from time import perf_counter, sleep


class User:
    """Represent a user in the application."""

    def __init__(self, username: str) -> None:
        """Initialize User instances."""
        self.username = username
        self.profile_data = self._get_profile_data()
        print(f"User {self.username} has been initialized")

    def _get_profile_data(self) -> str:
        print(f">>> Retrieving {self.username}'s profile data from the server")
        sleep(1)  # Simulate a network delay
        return f"profile data for {self.username}"


class UserV2:
    """Represent a user in the application (with lazy attributes)."""

    def __init__(self, username: str) -> None:
        """Initialize User instances."""
        self.username = username
        print(f"User {self.username} has been initialized")

    def __getattr__(self, attr_name: str) -> object:
        """Handle missing attributes, enabling lazy loading of profile_data."""
        if attr_name == "profile_data":
            print(f">> getattr: Loading profile data for {self.username}")
            self.profile_data = self._get_profile_data()
            return self.profile_data
        return None

    def _get_profile_data(self) -> str:
        print(f">>> Retrieving {self.username}'s profile data from the server")
        sleep(1)  # Simulate a network delay
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


def main() -> None:
    """Application entry point."""
    emma = User("Emma")
    print(">>> About to retrieve Emma's followers: 1st access")
    start_t = perf_counter()
    _ = get_followers(emma.username)
    end_t = perf_counter()
    print(f">>> Retrieved {emma.username}'s followers in {end_t - start_t:.2f} seconds")
    print("=" * 30)
    print(">>> About to retrieve Emma's followers: 2nd access")
    start_t = perf_counter()
    _ = get_followers(emma.username)
    end_t = perf_counter()
    print(f">>> Retrieved {emma.username}'s followers in {end_t - start_t:.2f} seconds")

    print("=" * 30)
    # Now using UserV2 which features lazy attributes
    alice = UserV2("Alice")
    print(">>> About to retrieve Alice's followers: 1st access")
    start_t = perf_counter()
    followers = get_followers_v2(alice.username)
    end_t = perf_counter()
    print(
        f">>> Retrieved {alice.username}'s followers in {end_t - start_t:.2f} seconds",
    )

    # Because the attributes are now lazily evaluated, it takes no time to get
    # the followers.
    # Only when the profile data is explicitly invoked the time will be spent,
    # and only once
    print("About to access Alice's profile_data:")
    start_t = perf_counter()
    _ = alice.profile_data
    print(f"Time to get profile_data: {perf_counter() - start_t:.2f} seconds")

    print("About to access Alice's profile_data: (2nd time)")
    start_t = perf_counter()
    _ = alice.profile_data
    print(f"Time to get profile_data: {perf_counter() - start_t:.2f} seconds")

    # Same thing for the followers, we will only evaluate their profile_data
    # when explicitly accessed
    start_t = perf_counter()
    print(f"{followers[0].username}'s profile data: {followers[0].profile_data}")
    print(f"Time to get profile_data: {perf_counter() - start_t:.2f} seconds")

    # But if we access follower's username we won't get penalized
    start_t = perf_counter()
    print(f"{followers[1].username}'s username: {followers[1].username}")
    print(f"Time to get username: {perf_counter() - start_t:.2f} seconds")


if __name__ == "__main__":
    main()
