""" script - illustrates fileinput module capabilities """
import fileinput

def main():
    for line in fileinput.input():
        if not line.startswith('#'):
            if fileinput.isfirstline():
                print("<start of file {0}>".format(fileinput.filename()))
            print(f"{"<stdin>" if fileinput.isstdin() else ""} | {fileinput.lineno()} | {fileinput.filelineno()}  >> {line}", end='')


if __name__ == '__main__':
    main()