#!/usr/bin/env python
"""Filters the data as per instructions."""

import fileinput

def main():
    for line in fileinput.input():
        (graphemes, phonemes) = line.rstrip().split("\t", 1)
        if len(graphemes) < 3 or " " in graphemes:
            continue
        print(f"{graphemes}\t{phonemes}")


if __name__ == "__main__":
    main()
