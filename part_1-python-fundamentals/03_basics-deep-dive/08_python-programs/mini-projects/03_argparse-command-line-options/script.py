""" script - illustrates basic argparse usage """
from argparse import ArgumentParser

def main():
    parser = ArgumentParser()
    parser.add_argument("indent", type=int, help="indent value for the report")
    parser.add_argument("input_file", help="file from where data is read from")

    # Optional arguments
    parser.add_argument("-f", "--file", dest="filename", help="file where report is written to")
    parser.add_argument("-x", "--xray", help="specify xray strength factor")
    parser.add_argument("-q", "--quiet", action="store_false", dest="verbose", default=True, help="don't print status messages to stdout")

    args = parser.parse_args()

    print("arguments:", args)

if __name__ == '__main__':
    main()