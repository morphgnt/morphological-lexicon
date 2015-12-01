#!/usr/bin/env python3

import re

S1_REGEX = [
    r"\w+$",
    r"(\w+)/(\w+)$",
    r"(\w+)\(ν\)$",
]

S2_REGEX = [
    r"G\d+$",
    r"\?$",
    r"G\d+(,G\d+)+$",
]

with open("abbott_smith_headwords.txt") as f:
    for line in f:
        s = line.strip().split("|")

        success = False
        for regex in S1_REGEX:
            if re.match(regex, s[0]):
                success = True
                break
        if not success:
            print("column 1:", s[1])
            quit()

        success = False
        for regex in S2_REGEX:
            if re.match(regex, s[1]):
                success = True
                break
        if not success:
            print("column 2:", s[1])
            quit()

print("success!")
