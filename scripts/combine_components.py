#!/usr/bin/env python

from pyuca import Collator
collator = Collator()

from morphgnt.utils import load_yaml
from morphgnt.utils import nfkc_normalize as n

danker = load_yaml("../data-cleanup/danker-concise-lexicon/components.yaml")

greenlee = {}
with open("../data-cleanup/greenlee-morphology/morphemes-utf8.txt") as f:
    for line in f:
        key, value = line.strip().split("\t")
        greenlee[n(key.decode("utf-8")).split(",")[0]] = {
            "full-entry": n(key.decode("utf-8")),
            "components": n(value.decode("utf-8")),
        }

words = [n(word) for word in set(danker.keys()).union(set(greenlee.keys()))]

for word in sorted(words, key=collator.sort_key):
    print "{}:".format(word.encode("utf-8"))
    if word in danker:
        print "    danker-full-entry: \"{}\"".format(danker[word]["full-entry"].encode("utf-8"))
        print "    danker-components: \"{}\"".format(danker[word]["components"].encode("utf-8"))
    if word in greenlee:
        print "    greenlee-full-entry: \"{}\"".format(greenlee[word]["full-entry"].encode("utf-8"))
        print "    greenlee-components: \"{}\"".format(greenlee[word]["components"].encode("utf-8"))
