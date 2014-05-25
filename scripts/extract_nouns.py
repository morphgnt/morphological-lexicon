#!/usr/bin/env python3

from collections import defaultdict

from morphgnt.utils import load_yaml
from morphgnt import filesets

lexemes = load_yaml("lexemes.yaml")

fs = filesets.load("filesets.yaml")

counts = defaultdict(int)

for row in fs["sblgnt-lexemes"].rows():
    if row["ccat-pos"] == "N-":
        counts[row["lemma"]] += 1


for lemma, count in sorted(
    counts.items(), key=lambda t: (t[1], t[0]), reverse=True
):
    lexemes_entry = lexemes.get(lemma, {"gloss": None})
    gloss = lexemes_entry.get("gloss")
    print("{}|{}|{}".format(lemma, count, gloss))
