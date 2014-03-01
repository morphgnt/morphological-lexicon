#!/usr/bin/env python
# coding: utf-8

from collections import defaultdict
import re
import sys
import unicodedata


from morphgnt import filesets
from morphgnt.utils import sorted_items


fs = filesets.load("filesets.yaml")


ACUTE = u"\u0301"
GRAVE = u"\u0300"
CIRCUMFLEX = u"\u0342"


def strip_accents(w):
    return "".join(
        unicodedata.normalize("NFC", "".join(
            component for component in unicodedata.normalize("NFD", ch) if component not in [ACUTE, GRAVE, CIRCUMFLEX]
        )) for ch in w
    )


# tense_voice -> list of dicts mapping person_number to ending (or ?)
ENDINGS = defaultdict(list)

with open("ending-paradigms.txt") as f:
    num = 0
    for line in f:
        num += 1
        tense_voice, rest = line.strip().split(":")
        endings = dict(zip(["1S", "2S", "3S", "1P", "2P", "3P", "num"], [i.strip() for i in rest.split(",")] + [num]))
        ENDINGS[tense_voice].append(endings)


fs = filesets.load("filesets.yaml")

# lemma -> tense_voice -> person_number -> set of forms
forms = defaultdict(lambda: defaultdict(lambda: defaultdict(set)))


def equal(lst):
    """
    are all elements of lst equal?
    """
    return lst.count(lst[0]) == len(lst)


for row in fs["sblgnt-lexemes"].rows():
    if row["ccat-pos"] == "V-":
        mood = row["ccat-parse"][3]
        if mood in "I":
            person_number = row["ccat-parse"][0] + row["ccat-parse"][5]
            tense_voice = row["ccat-parse"][1:3]
            forms[row["lemma"]][tense_voice][person_number].add(strip_accents(row["norm"]))
        elif mood in "DSO":
            pass
        elif mood in "P":
            pass
        elif mood in "N":
            pass
        else:
            raise ValueError


for lemma, form_dict in sorted_items(forms):
    for tense_voice in sorted(form_dict):
        print()
        print(lemma, tense_voice, len(form_dict[tense_voice]))
        stem_rules = []
        print(form_dict[tense_voice])
        for endings in ENDINGS[tense_voice]:
            fail = False
            stems = []
            num = endings["num"]
            print("\t", num, endings)
            for person_number, ending in sorted(endings.items()):
                if person_number == "num":
                    continue
                print("\t\t\t", person_number, ending)
                ending = sorted(ending.split("/"))
                x = sorted(form_dict[tense_voice].get(person_number, "?"))
                if ending == ["?"] or x == ["?"]:
                    print("\t\t\t\tskip because of ?")
                    continue
                if len(ending) != len(x):
                    fail = True
                    print("\t\t\t\tfail because len", ending, "!= len", x)
                    break
                stem_possibilities = set()
                for a, b in zip(ending, x):
                    print("\t\t\t\t\ttesting", a, b)
                    regex = a.replace("?", "\\?").replace("(", "\\(").replace(")", "\\)") + "$"
                    if not re.search(regex, b):
                        fail = True
                        break
                    print("\t\t\t", person_number, a, b, re.sub(regex, "", b))
                    stem_possibilities.add(re.sub(regex, "", b))
                if len(stem_possibilities) == 1:
                    stems.append(list(stem_possibilities)[0])
                else:
                    fail = True
                    break
            print("\t\t", stems, fail)
            if stems and not fail and equal(stems):
                stem_rules.append((num, stems[0], len(stems)))

        if len(stem_rules) == 0:
            print(form_dict[tense_voice])
            print("no rules matched")
            sys.exit(1)
        for rule, stem, count in stem_rules:
            print("\t", rule, stem, count)
