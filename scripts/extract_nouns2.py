#!/usr/bin/env python3

from collections import defaultdict

from morphgnt.utils import load_yaml
from morphgnt import filesets

lexemes = load_yaml("lexemes.yaml")

fs = filesets.load("filesets.yaml")

# lemma -> form -> cng -> count
forms = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))

for row in fs["sblgnt-lexemes"].rows():
    if row["ccat-pos"] == "N-":
        forms[row["lemma"]][row["norm"]][row["ccat-parse"][4:7]] += 1


for lemma in forms:
    lexemes_entry = lexemes.get(lemma, {"mounce-morphcat": None})
    morphcat = lexemes_entry.get("mounce-morphcat")
    form_list = []
    for form in forms[lemma]:
        for parse in forms[lemma][form]:
            form_list.append("{}:{}:{}".format(
                form, parse, forms[lemma][form][parse]
            ))
    print("{}|{}|{}".format(lemma, morphcat, "/".join(form_list)))
