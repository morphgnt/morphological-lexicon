#!/usr/bin/env python

from morphgnt import filesets
from morphgnt.utils import load_yaml

lexemes = load_yaml("lexemes.yaml")
fs = filesets.load("filesets.yaml")

total = 0
match = 0
first_fail = None

for row in fs["sblgnt-lexemes"].rows():
    total += 1
    if row["lemma"].decode("utf-8") in lexemes:
        match += 1
    elif first_fail is None:
        first_fail = "{} {} {}".format(row["lemma"], row["ccat-pos"], row["robinson"])

print "{}/{} = {}%".format(match, total, int(1000 * match / total) / 10)
if first_fail:
    print first_fail
