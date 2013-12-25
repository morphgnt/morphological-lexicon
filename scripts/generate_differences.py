#!/usr/bin/env python
# coding: utf-8

from collections import defaultdict
import sys
import unicodedata

from morphgnt.utils import load_yaml, sorted_items

lexemes = load_yaml("lexemes.yaml")


def strip_accents(s):
    return "".join((c for c in unicodedata.normalize("NFD", unicode(s)) if unicodedata.category(c) != "Mn"))


METADATA_NAMES = [
    "bdag-headword",
    "danker-entry",
    "dodson-entry",
    "mounce-headword",
]

fully_match = 0
no_tag = 0

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
            elif value.replace(u"οε", u"ου") == lexeme:
                tags.append("οε contraction")
            elif value.replace(u"ω", u"ομαι") == lexeme:
                tags.append("ω/ομαι")
            elif strip_accents(value).replace(u"ος", u"οτερος") == strip_accents(lexeme):
                tags.append("-τερος")
            else:
                if value != "<missing>":
                    tags.append("@@@")
                    no_tag += 1
            print "    {}:".format(value.encode("utf-8"))
            print "        {}: [{}]".format("tags", ", ".join("\"{}\"".format(tag) for tag in tags))
            print "        {}: [{}]".format("sources", ", ".join("\"{}\"".format(source) for source in metadata_names))
    else:
        fully_match += 1

print >>sys.stderr, "{} fully-match; {} no-tag".format(fully_match, no_tag)
