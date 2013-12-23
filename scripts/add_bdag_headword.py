#!/usr/bin/env python

import sys

from pyuca import Collator
collator = Collator()

from morphgnt.utils import load_yaml, load_wordset
from morphgnt.utils import nfkc_normalize as n

lexemes = load_yaml("lexemes.yaml")
missing_bdag = load_wordset("missing_bdag.txt")


headwords = set()
with open("../data-cleanup/bdag-headwords/bdag_headwords.txt") as f:
    for line in f:
        headwords.add(n(line.strip().decode("utf-8")))

existing_not_in_headwords = []
missing_not_in_headwords = []
added = []
for lexeme, metadata in sorted(lexemes.items(), key=lambda x: collator.sort_key(x[0])):
    print "{}:".format(lexeme.encode("utf-8"))
    print "    pos: {}".format(metadata["pos"])
    
    if "bdag-headword" in metadata:
        print "    bdag-headword: {}".format(metadata["bdag-headword"].encode("utf-8"))
        if metadata["bdag-headword"] not in headwords:
            existing_not_in_headwords.append(metadata["bdag-headword"].encode("utf-8"))
    else:
        if lexeme in headwords:
            print "    bdag-headword: {}".format(lexeme.encode("utf-8"))
            added.append(lexeme.encode("utf-8"))
        else:
            missing_not_in_headwords.append(lexeme.encode("utf-8"))
    
    def q(metadata_name):
        if metadata_name in metadata:
            print "    {}: {}".format(metadata_name, unicode(metadata[metadata_name]).encode("utf-8"))
    
    q("dodson-entry")
    q("strongs")
    q("gk")
    q("dodson-pos")
    q("gloss")
    q("mounce-morphcat")


print >>sys.stderr, "existing"
for word in existing_not_in_headwords:
    print >>sys.stderr, "\t", word
print >>sys.stderr, "missing"
for word in missing_not_in_headwords:
    if word.decode("utf-8") not in missing_bdag:
        print >>sys.stderr, "\t", word
print >>sys.stderr, "added"
for word in added:
    print >>sys.stderr, "\t", word
print >>sys.stderr, "{} {} {}".format(len(existing_not_in_headwords), len(missing_not_in_headwords), len(added))
