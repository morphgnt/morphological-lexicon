#!/usr/bin/env python

import sys

from morphgnt.utils import nfkc_normalize

with open(sys.argv[1]) as f:
    for line in f:
        sys.stdout.write(nfkc_normalize(line.decode("utf-8")).encode("utf-8"))
