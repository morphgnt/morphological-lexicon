#!/usr/bin/env python

from collections import defaultdict
import sys

from morphgnt.utils import load_yaml, sorted_items, load_wordset
from morphgnt.utils import nfkc_normalize as n

lexemes = load_yaml("lexemes.yaml")
missing_mounce = load_wordset("missing_mounce.txt")

problems = []
skipped = 0

mounce = defaultdict(list)
with open("../data-cleanup/mounce-morphcat/mounce-tauber-morphcat-utf8.txt") as f:
    for line in f:
        gk, greek, morphcat = line.strip().decode("utf-8").split(":")
        mounce[int(gk.split("?")[0])].append(n(greek))

for lexeme, metadata in sorted_items(lexemes):
    print "{}:".format(lexeme.encode("utf-8"))

    def q(metadata_name):
        if metadata_name in metadata:
            print "    {}: {}".format(metadata_name, unicode(metadata[metadata_name]).encode("utf-8"))
            return True

    q("pos")
    q("bdag-headword")
    q("danker-entry")
    q("dodson-entry")

    if not q("mounce-headword"):
        if lexeme in missing_mounce:
            skipped += 1
            continue
        k = metadata.get("gk")
        if isinstance(k, list):
            k = ", ".join(str(i) for i in k)
        v = mounce.get(k)
        if v:
            if len(v) == 1:
                v = v[0]
            else:
                v = ", ".join(v)
            print "    {}: {}".format("mounce-headword", v.encode("utf-8"))
        else:
            problems.append("{} {} not found".format(lexeme.encode("utf-8"), k))

    q("strongs")
    q("gk")
    q("dodson-pos")
    q("gloss")
    q("mounce-morphcat")


print >>sys.stderr, "problems"
for problem in problems:
    print >>sys.stderr, "\t", problem
print >>sys.stderr, "{} ({} skipped)".format(len(problems), skipped)
