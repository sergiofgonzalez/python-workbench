""" script that """
import sys

def main():
    contents = sys.stdin.read() # reads from stdin
    sys.stdout.write(contents.replace(sys.argv[1], sys.argv[2])) # writes to stdout


if __name__ == "__main__":
    main()