"""Illustrate the use of argparse for basic CLI scripts."""

import argparse


def main() -> None:
    """Application entry point."""
    parser = argparse.ArgumentParser(
        description="This script returns a greeting for the user.",
    )
    parser.add_argument(
        "--name",
        "-n",
        metavar="NAME", # how it is displayed in help msg
        type=str,
        required=True,
        help="The name of the person to be greeted", # will show when using --help
    )
    parser.add_argument(
        "--type",
        "-t",
        choices=["formal", "informal", "friendly"],
        metavar="GREETING_TYPE", # how it is displayed in help msg
        type=str,
        default="friendly", # default value if not provided
        help="The type of greeting to use", # will show when using --help
    )

    args = parser.parse_args()
    print("Arguments received:", args.name, args.type)

    if args.type == "formal":
        print(f"Good day, {args.name}.")
    elif args.type == "informal":
        print(f"Hey {args.name}!")
    elif args.type == "friendly":
        print(f"Hello {args.name}, it's great to see you!")

if __name__ == "__main__":
    main()
