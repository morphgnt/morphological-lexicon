#!/usr/bin/env python3

with open("abbott_smith_headwords.txt") as f:
    for line in f:
        s = line.strip().split("|")
        if len(s) != 3:
            print(line.strip())
