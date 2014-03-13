#!/usr/bin/env python

import sys

from pyuca import Collator
collator = Collator()

with open(sys.argv[1]) as f:
    lines = f.readlines()
    for line in sorted(lines, key=collator.sort_key):
        sys.stdout.write(line)
