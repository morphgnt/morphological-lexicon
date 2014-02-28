#!/usr/bin/env python
# coding: utf-8

from collections import defaultdict
import sys
import unicodedata


from morphgnt import filesets

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


# lemma -> tense_voice -> person_number -> set of forms
forms = defaultdict(lambda: defaultdict(lambda: defaultdict(set)))

# tense_voice -> person_number -> set of ending paradigms
paradigms = defaultdict(lambda: defaultdict(set))


fs = filesets.load("filesets.yaml")

for row in fs["sblgnt-lexemes"].rows():
    if row["ccat-pos"] == "V-":
        mood = row["ccat-parse"][3]
        if mood in "I":
            person_number = row["ccat-parse"][0] + row["ccat-parse"][5]
            tense_voice = row["ccat-parse"][1:3]
            forms[row["lemma"]][tense_voice][person_number].add(strip_accents(row["norm"].decode("utf-8")))
        elif mood in "DSO":
            pass
        elif mood in "P":
            pass
        elif mood in "N":
            pass
        else:
            raise ValueError


def equal(lst):
    """
    are all elements of lst equal?
    """
    return lst.count(lst[0]) == len(lst)


def to_tuple(d):
    if len([i for s in d.values() for i in s]) == 1:
        return ()
    for offset in range(max(len(i) for s in d.values() for i in s)):
        if equal([i[:offset] for s in d.values() for i in s]):
            continue
        else:
            break
    return (
        ("/".join(i[offset - 1:] for i in d["1S"]) if "1S" in d else "?"),
        ("/".join(i[offset - 1:] for i in d["2S"]) if "2S" in d else "?"),
        ("/".join(i[offset - 1:] for i in d["3S"]) if "3S" in d else "?"),
        ("/".join(i[offset - 1:] for i in d["1P"]) if "1P" in d else "?"),
        ("/".join(i[offset - 1:] for i in d["2P"]) if "2P" in d else "?"),
        ("/".join(i[offset - 1:] for i in d["3P"]) if "3P" in d else "?"),
    )

endings = defaultdict(set)

for lemma in forms:
    for tense_voice in forms[lemma]:
        t = to_tuple(forms[lemma][tense_voice])
        if t:
            endings[tense_voice].add(t)


for tense_voice in endings:
    for t in endings[tense_voice]:
        print tense_voice, t.count("?"), ", ".join(i.encode("utf-8") for i in t)
