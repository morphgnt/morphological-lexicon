#!/usr/bin/env python

import sys
import unicodedata

from pyuca import Collator
collator = Collator()

from morphgnt.utils import load_yaml

def n(x):
    return unicodedata.normalize("NFKC", x)

lexemes = load_yaml("lexemes.yaml")

headwords = set()
with open("../data-cleanup/bdag-headwords/bdag_headwords.txt") as f:
    for line in f:
        headwords.add(n(line.strip().decode("utf-8")))

existing_not_in_headwords = []
missing_not_in_headwords = []
added = []
for lexeme, metadata in sorted(lexemes.items(), key=lambda x: collator.sort_key(x[0])):
    if "bdag-headword" in metadata:
        print "{}:\n    pos: {}\n    bdag-headword: {}".format(lexeme.encode("utf-8"), metadata["pos"], metadata["bdag-headword"].encode("utf-8"))
        if metadata["bdag-headword"] not in headwords:
            existing_not_in_headwords.append(metadata["bdag-headword"].encode("utf-8"))
    else:
        if lexeme in headwords:
            print "{}:\n    pos: {}\n    bdag-headword: {}".format(lexeme.encode("utf-8"), metadata["pos"], lexeme.encode("utf-8"))
            added.append(lexeme.encode("utf-8"))
        else:
            print "{}:\n    pos: {}".format(lexeme.encode("utf-8"), metadata["pos"])
            missing_not_in_headwords.append(lexeme.encode("utf-8"))

print >>sys.stderr, "existing"
for word in existing_not_in_headwords:
    print >>sys.stderr, "\t", word
print >>sys.stderr, "missing"
for word in missing_not_in_headwords:
    print >>sys.stderr, "\t", word
print >>sys.stderr, "added"
for word in added:
    print >>sys.stderr, "\t", word
print >>sys.stderr, "{} {} {}".format(len(existing_not_in_headwords), len(missing_not_in_headwords), len(added))
