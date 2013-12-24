#!/usr/bin/env python

from collections import defaultdict
import sys
import unicodedata

from morphgnt.utils import load_yaml, sorted_items

lexemes = load_yaml("lexemes.yaml")

fully_match = 0


def strip_accents(s):
    return "".join((c for c in unicodedata.normalize("NFD", unicode(s)) if unicodedata.category(c) != "Mn"))


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

    differences = defaultdict(list)
    for metadata_name in METADATA_NAMES:
        if r(metadata_name):
            differences[r(metadata_name)].append(metadata_name)

    if differences:
        print "{}:".format(lexeme.encode("utf-8"))
        for value, metadata_names in differences.items():
            tags = []
            if value.lower() == lexeme.lower():
                tags.append("case")
            elif strip_accents(value) == strip_accents(lexeme):
                tags.append("accentuation")
            elif strip_accents(value.lower()) == strip_accents(lexeme.lower()):
                tags.append("case")
                tags.append("accentuation")
            print "    {}:".format(value.encode("utf-8"))
            print "        {}: {}".format("tags", ", ".join(tags))
            print "        {}: {}".format("sources", ", ".join(metadata_names))
    else:
        fully_match += 1

print >>sys.stderr, "{} fully-match".format(fully_match)
