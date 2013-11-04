#!/usr/bin/env python

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

for lexeme, metadata in sorted(lexemes.items(), key=lambda x: collator.sort_key(x[0])):
    if lexeme in headwords:
        print "{}:\n    pos: {}\n    bdag-headword: {}".format(lexeme.encode("utf-8"), metadata["pos"], lexeme.encode("utf-8"))
    else:
        print "{}:\n    pos: {}\n    bdag-headword: @@@".format(lexeme.encode("utf-8"), metadata["pos"])
