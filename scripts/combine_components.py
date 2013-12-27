#!/usr/bin/env python

from morphgnt.utils import load_yaml
from morphgnt.utils import nfkc_normalize as n

danker = load_yaml("../data-cleanup/danker-concise-lexicon/components.yaml")

greenlee = {}
with open("../data-cleanup/greenlee-morphology/morphemes-utf8.txt") as f:
    for line in f:
        key, value = line.strip().split("\t")
        greenlee[n(key.decode("utf-8").split(",")[0])] = {
            "full-entry": n(key.decode("utf-8")),
            "components": n(value.decode("utf-8")),
        }
