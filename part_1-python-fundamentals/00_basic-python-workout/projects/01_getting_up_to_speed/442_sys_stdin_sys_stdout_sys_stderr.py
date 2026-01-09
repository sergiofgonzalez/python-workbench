"""Playing with sys.stdin, sys.stdout, and sys.stderr."""

import sys


def main() -> None:
    """Application entry point."""
    # read user input from stdin
    print("Reading input with sys.stdin.read() (use Ctrl-D or Ctrl-Z to end input):")
    print("Please type your name:")
    user_name = sys.stdin.read()
    print("Please type your age:")
    user_age = sys.stdin.read()
    print(f">>> {user_name!r}")
    print(f">>> {user_age!r}")

    print("Reading input with sys.stdin.readline() (use Enter to end input):")
    print("Please type your name:")
    user_name = sys.stdin.readline()
    print("Please type your age:")
    user_age = sys.stdin.readline()
    print(f">>> {user_name!r}")
    print(f">>> {user_age!r}")

    # Treating stdout and stderr as files
    age = int(user_age.strip())
    if age > 18:  # noqa: PLR2004
        sys.stdout.write(
            f"Welcome, {user_name.strip()}! You are an adult of {age} years of age.\n",
        )
    else:
        sys.stderr.write(
            f"Sorry, {user_name.strip()}, you are not an adult. "
            f"You are {age} years old.\n",
        )


if __name__ == "__main__":
    main()
