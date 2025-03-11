#!/usr/bin/env python3
"""
simplified version of the 'wc' utility that counts lines, words, and bytes.
- for every file, shows number of lines, words, bytes, and filename
- when multiple files provided, shows total count at the end
- when no files provided, reads from stdin and shows counts without filename
"""

import sys

def count_file_stats(file_obj):
    """
    counts the number of lines, words, and bytes in the given file object.
    
    args:
        file_obj: file like object to read from it
        
    returns:
        tuple of (line_count, word_count, byte_count)
    """
    content = file_obj.read()
    lines = content.count('\n')
    words = len(content.split())
    # count bytes, not characters
    bytes_count = len(content.encode('utf-8'))
    
    return lines, words, bytes_count

def print_stats(stats, filename=None):
    """
    prints statistics in format used by wc.
    
    args:
        stats: tuple of (line_count, word_count, byte_count)
        filename: optional filename to display
    """
    line_count, word_count, byte_count = stats
    if filename:
        print(f"{line_count:8d} {word_count:8d} {byte_count:8d} {filename}")
    else:
        print(f"{line_count:8d} {word_count:8d} {byte_count:8d}")

def main():
    # when no files provided, read from stdin
    if len(sys.argv) == 1:
        stats = count_file_stats(sys.stdin)
        print_stats(stats)
        return
    
    # keep track of totals
    total_lines = 0
    total_words = 0
    total_bytes = 0
    
    for filename in sys.argv[1:]:
        try:
            with open(filename, 'r') as file:
                stats = count_file_stats(file)
                print_stats(stats, filename)
                total_lines += stats[0]
                total_words += stats[1]
                total_bytes += stats[2]
                
        except FileNotFoundError:
            print(f"{filename}: No such file or directory", file=sys.stderr)
            sys.exit(1)
    
    # when multiple files processed, we also print total res
    if len(sys.argv) > 2:
        print_stats((total_lines, total_words, total_bytes), "total")

if __name__ == "__main__":
    main()