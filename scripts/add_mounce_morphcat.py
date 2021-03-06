#!/usr/bin/env python

from collections import defaultdict
import sys

from morphgnt.utils import load_yaml, load_wordset, sorted_items
from morphgnt.utils import nfkc_normalize as n

lexemes = load_yaml("lexemes.yaml")
missing_morphcat = load_wordset("missing_morphcat.txt")

mounce = defaultdict(list)
with open("../data-cleanup/mounce-morphcat/mounce-tauber-morphcat-utf8.txt") as f:
    for line in f:
        gk, greek, morphcat = line.strip().decode("utf-8").split(":")
        greek = n(greek)
        mounce[greek].append({
            "gk": gk,
            "morphcat": morphcat,
        })

problems = []
skipped = 0
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
    q("mounce-headword")
    q("strongs")
    q("gk")
    q("dodson-pos")
    q("gloss")

    if not q("mounce-morphcat"):
        if lexeme in missing_morphcat:
            skipped += 1
            continue
        if lexeme in mounce:
            source = lexeme
        elif metadata.get("bdag-headword") in mounce:
            source = metadata["bdag-headword"]
        else:
            source = None
        if source:
            if len(mounce[source]) == 1:
                try:
                    gk = int(mounce[source][0]["gk"])
                except ValueError:
                    gk = None
                if metadata.get("gk") == gk:
                    print "    mounce-morphcat: {}".format(mounce[source][0]["morphcat"])
                else:
                    problems.append("{} {} != {}".format(source.encode("utf-8"), metadata.get("gk"), gk))
            else:
                problems.append("{} len({}) > 1".format(source.encode("utf-8"), mounce[source]))
        else:
            problems.append("{} not found (gk={})".format(lexeme.encode("utf-8"), metadata.get("gk")))


print >>sys.stderr, "problems"
for problem in problems:
    print >>sys.stderr, "\t", problem
print >>sys.stderr, "{} ({} skipped)".format(len(problems), skipped)
