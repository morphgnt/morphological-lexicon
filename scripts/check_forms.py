#!/usr/bin/env python

from morphgnt import filesets
from morphgnt.utils import load_yaml

lexemes = load_yaml("lexemes.yaml")
forms = load_yaml("forms.yaml")
fs = filesets.load("filesets.yaml")

total = 0
match = 0
first_fail = None

for row in fs["sblgnt-forms"].rows():
    total += 1
    lexeme = lexemes.get(row["lemma"].decode("utf-8"))
    success = False
    if lexeme:
        form_entry = forms.get(row["lemma"].decode("utf-8"))
        if form_entry:
            if lexeme["pos"] in ["RA", "A", "N", "RR"]:
                try:
                    expected_form = form_entry[row["ccat-parse"][6]][row["ccat-parse"][4:6]]["form"]
                    if expected_form == row["norm"].decode("utf-8"):
                        success = True
                except KeyError:
                    pass
            elif lexeme["pos"] in ["RP1"]:
                try:
                    expected_form = form_entry[row["ccat-parse"][4:6]]["form"]
                    if expected_form == row["norm"].decode("utf-8"):
                        success = True
                except KeyError:
                    pass
            elif lexeme["pos"] in ["V"]:
                if row["ccat-parse"][3] in ["I"]:
                    try:
                        expected_form = form_entry[row["ccat-parse"][1:4]][row["ccat-parse"][0] + row["ccat-parse"][5]]["form"]
                        if expected_form == row["norm"].decode("utf-8"):
                            success = True
                    except KeyError:
                        pass
            elif lexeme["pos"] in "P":
                try:
                    expected_form = form_entry["form"]
                    if expected_form == row["norm"].decode("utf-8"):
                        success = True
                except KeyError:
                    pass
    if success:
        match += 1
    else:
        if first_fail is None:
            first_fail = "{} {} {} {} {}".format(row["norm"], row["ccat-pos"], row["ccat-parse"], row["robinson"], row["lemma"])


print "{}/{} = {}%".format(match, total, int(1000 * match / total) / 10)
if first_fail:
    print first_fail
