#!/usr/bin/env python

import sys

from morphgnt.utils import load_yaml, sorted_items

lexemes = load_yaml("lexemes.yaml")

fully_match = 0

METADATA_NAMES = [
    "bdag-headword",
    "danker-entry",
    "dodson-entry",
    "mounce-headword",
]

for lexeme, metadata in sorted_items(lexemes):

    def r(metadata_name):
        v = metadata.get(metadata_name, "<missing>")
        if v:
            v = v.split(",")[0]
        return v if v != lexeme else None

    differences = {
        k: r(k) for k in METADATA_NAMES
    }

    if any(differences.values()):
        print "{}:".format(lexeme.encode("utf-8"))
        for metadata_name in METADATA_NAMES:
            if differences[metadata_name]:
                print "    {}:".format(metadata_name)
                print "        value: {}".format(differences[metadata_name].encode("utf-8"))
    else:
        fully_match += 1

print >>sys.stderr, "{} fully-match".format(fully_match)
