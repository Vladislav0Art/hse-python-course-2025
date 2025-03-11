#!/usr/bin/env python3
"""
simplified version of the 'tail' utility that shows the last lines of files or stdin.
- when files provided, shows last 10 lines of each file
- when multiple files provided, shows filename before each file content
- when no files provided, shows last 17 lines from stdin
"""

import sys

def tail_file(file_obj, num_lines=10):
    """
    returns last num_lines lines from the given file object.
    
    args:
        file_obj: A file-like object to read lines from
        num_lines: Number of lines to return from the end
        
    returns:
        A list of the last num_lines lines
    """
    lines = file_obj.readlines()
    return lines[-num_lines:] if lines else []

def main():
    if len(sys.argv) == 1:
        for line in tail_file(sys.stdin, num_lines=17):
            print(line, end="")
        return
    
    for i, filename in enumerate(sys.argv[1:]):
        try:
            # print header before every file to separate them
            if i > 0: print()
            # when many files, print filename header also
            if len(sys.argv) > 2:
                print(f"==> {filename} <==")
            
            with open(filename, 'r') as file:
                for line in tail_file(file, 10):
                    print(line, end="")
                    
        except FileNotFoundError:
            print(f"cannot open '{filename}' for reading: No such file or directory", file=sys.stderr)
            sys.exit(1)

if __name__ == "__main__":
    main()