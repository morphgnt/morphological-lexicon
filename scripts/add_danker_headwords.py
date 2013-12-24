#!/usr/bin/env python

import sys

from morphgnt.utils import load_yaml, load_wordset, sorted_items

lexemes = load_yaml("lexemes.yaml")
danker = load_yaml("../data-cleanup/danker-concise-lexicon/danker_headwords.yaml")
missing_danker = load_wordset("missing_danker.txt")

problems = []
skipped = 0

for lexeme, metadata in sorted_items(lexemes):
    print "{}:".format(lexeme.encode("utf-8"))

    def q(metadata_name):
        if metadata_name in metadata:
            print "    {}: {}".format(metadata_name, unicode(metadata[metadata_name]).encode("utf-8"))

    q("pos")
    q("bdag-headword")

    if "danker-entry" in metadata:
        print "    {}: {}".format("danker-entry", metadata["danker-entry"].encode("utf-8"))
    else:
        if lexeme in missing_danker:
            skipped += 1
        else:
            if lexeme in danker:
                entry = danker[lexeme]
            elif metadata.get("bdag-headword") in danker:
                entry = danker[metadata["bdag-headword"]]
            else:
                entry = None

            if entry:
                print "    {}: {}".format("danker-entry", entry.encode("utf-8"))
            else:
                problems.append("{} not found (bdag={})".format(lexeme.encode("utf-8"), metadata.get("bdag-headword", u"none").encode("utf-8")))

    q("dodson-entry")
    q("strongs")
    q("gk")
    q("dodson-pos")
    q("gloss")
    q("mounce-morphcat")


print >>sys.stderr, "problems"
for problem in problems:
    print >>sys.stderr, "\t", problem
print >>sys.stderr, "{} ({} skipped)".format(len(problems), skipped)
