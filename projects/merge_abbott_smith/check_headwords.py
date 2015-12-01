#!/usr/bin/env python3

import re

with open("abbott_smith_headwords.txt") as f:
    for line in f:
        s = line.strip().split("|")

        S1_REGEX = [
            r"\w+$",
            r"(\w+)/(\w+)$",
            r"(\w+)\(ν\)$",
        ]

        success = False
        for regex in S1_REGEX:
            if re.match(regex, s[0]):
                success = True
                break

        if not success:
            print(s[0])
            quit()

print("success!")
