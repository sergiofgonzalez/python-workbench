"""Illustrates how to add positional and optional args when using argparse."""

import argparse


def main() -> None:
    """Application entry point."""
    parser = argparse.ArgumentParser(
        # This will show when using -h/--help
        description="Demonstrate positional and optional arguments with argparse.",
    )

    # Positional arguments
    parser.add_argument(
        "indent",
        type=int,
        help="Number of spaces to indent.",
    )
    parser.add_argument(
        "input_file",
        type=str,
        help="Path to the file in which to apply indentation.",
    )

    # Optional arguments
    parser.add_argument(
        "-f",
        "--file-output",
        dest="filename",
        help="Path to the output file. Defaults to standard output.",
    )
    parser.add_argument(
        "-x",
        "--x-ray",
        help="X-ray strength factor.",
    )
    parser.add_argument(
        "-q",
        "--quiet",
        dest="verbose",
        action="store_false",
        default=True,
        help="Disable printing status messages to standard output.",
    )

    # Parse the arguments received from the command line
    args = parser.parse_args()
    print(f"{args=}")
    print("=" * 40)

    # Example usage of the parsed arguments using vars() to convert to a dictionary
    for arg_name, arg_value in vars(args).items():
        print(f"{arg_name}: {arg_value}")
    print("=" * 40)

    for arg_name, arg_value in args.__dict__.items():
        print(f"{arg_name}: {arg_value}")
    print("=" * 40)

    # You can access individual arguments like this:
    print(f"Indentation level: {args.indent}")
    print(f"Input file: {args.input_file}")
    if args.filename:
        print(f"Output file: {args.filename}")
    else:
        print("Output will be printed to standard output.")
    if args.verbose:
        print("Verbose mode is enabled.")
    else:
        print("Quiet mode is enabled.")
    if args.x_ray:
        print(f"X-ray strength factor: {args.x_ray}")
    else:
        print("No X-ray strength factor provided.")


if __name__ == "__main__":
    main()
