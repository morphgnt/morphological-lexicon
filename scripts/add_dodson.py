#!/usr/bin/env python

from collections import defaultdict
import sys

from pyuca import Collator
collator = Collator()

from morphgnt.utils import load_yaml, load_wordset
from morphgnt.utils import nfkc_normalize as n

lexemes = load_yaml("lexemes.yaml")
missing_dodson = load_wordset("missing_dodson.txt")

dodson = defaultdict(list)
with open("../data-cleanup/dodson-lexicon/dodson_lexicon.txt") as f:
    for line in f:
        strongs, gk, pos, greek, short_gloss, long_gloss = line.strip().decode("utf-8").split("\t")
        head_word = n(greek.split(",")[0])
        dodson[head_word].append({
            "strongs": strongs,
            "gk": gk,
            "pos": pos,
            "greek": n(greek),
            "short-gloss": short_gloss,
            "long-gloss": long_gloss
        })

not_in_dodson = set()
for lexeme, metadata in sorted(lexemes.items(), key=lambda x: collator.sort_key(x[0])):
    print "{}:".format(lexeme.encode("utf-8"))
    print "    pos: {}".format(metadata["pos"])
    
    def q(metadata_name):
        if metadata_name in metadata:
            print "    {}: {}".format(metadata_name, unicode(metadata[metadata_name]).encode("utf-8"))
    
    q("bdag-headword")
    q("danker-entry")
    
    if lexeme in dodson or metadata.get("bdag-headword") in dodson:
        if lexeme in dodson:
            data = dodson[lexeme]
        else:
            data = dodson[metadata["bdag-headword"]]
        if len(data) == 1:
            data = data[0]
        else:
            data = None
    else:
        data = None
    
    def p(metadata_name, data_name):
        if metadata_name in metadata:
            print "    {}: {}".format(metadata_name, unicode(metadata[metadata_name]).encode("utf-8"))
        else:
            if data:
                print "    {}: {}".format(metadata_name, data[data_name].encode("utf-8"))
            else:
                not_in_dodson.add(lexeme.encode("utf-8"))
    
    p("dodson-entry", "greek")
    p("strongs", "strongs")
    p("gk", "gk")
    p("dodson-pos", "pos")
    p("gloss", "short-gloss")
    
    q("mounce-morphcat")


print >>sys.stderr, "missing"
for word in not_in_dodson:
    if word.decode("utf-8") not in missing_dodson:
        print >>sys.stderr, "\t", word
print >>sys.stderr, "{}".format(len(not_in_dodson))
