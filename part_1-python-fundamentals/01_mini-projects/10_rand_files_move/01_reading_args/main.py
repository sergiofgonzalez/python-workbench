"""
CLI tool basics: reading args and such stuff
"""
import sys
import argparse


# Raw argument management
print(f"I've received {len(sys.argv[1:])} argument(s)")
for i, arg_str in enumerate(sys.argv[1:]):
    print(f"{i}: {arg_str}")


# Using argparse is a much better solution
parser = argparse.ArgumentParser(
    description="This program randomly picks files from a source folder and move them to a destination folder"
)

parser.add_argument(
    "-s",
    "--src",
    metavar="{source folder}",
    required=True,
    help="Source folder from where to pick up files",
)

parser.add_argument(
    "-d",
    "--dst",
    metavar="{destination folder}",
    required=True,
    help="Destination folders where files will be moved",
)

parser.add_argument(
    "-g",
    "--glob",
    metavar="{globbing pattern}",
    nargs="+",
    required=True,
    help="Pattern indicating the files that will be picked up"
)

args = parser.parse_args()


print(f"src : {args.src}")
print(f"dst : {args.dst}")
print(f"glob: {args.glob}")
