#!/usr/bin/env python3
"""
simplified version of the 'nl' utility that numbers all lines from a file or stdin. works like 'nl -b a'.
"""

import sys

def number_lines(file_obj):
    """
    number all lines from given file object and print them to stdout.
    
    args:
        file_obj: file-like object to read lines from it
    """
    line_num = 1
    for line in file_obj:
        print(f"{line_num:6d}\t{line}", end="")
        line_num += 1

def main():
    if len(sys.argv) > 1:
        try:
            with open(sys.argv[1], 'r') as file:
                number_lines(file)
        except FileNotFoundError:
            print(f"{sys.argv[1]}: No such file or directory", file=sys.stderr)
            sys.exit(1)
    else:
        number_lines(sys.stdin)

if __name__ == "__main__":
    main()