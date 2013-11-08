#!/usr/bin/env python

from collections import defaultdict
import sys
import unicodedata

from pyuca import Collator
collator = Collator()

from morphgnt.utils import load_yaml

def n(x):
    return unicodedata.normalize("NFKC", x)

lexemes = load_yaml("lexemes.yaml")

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
    if "bdag-headword" in metadata:
        print "    bdag-headword: {}".format(metadata["bdag-headword"].encode("utf-8"))
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


print >>sys.stderr, "missing"
for word in not_in_dodson:
    print >>sys.stderr, "\t", word
print >>sys.stderr, "{}".format(len(not_in_dodson))
