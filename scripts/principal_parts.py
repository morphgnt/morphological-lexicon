#!/usr/bin/env python
# coding: utf-8


from collections import defaultdict
import re
import unicodedata

from morphgnt import filesets

fs = filesets.load("filesets.yaml")

first_singular = defaultdict(lambda: defaultdict(set))


def strip_accents(s):
    return "".join((c for c in unicodedata.normalize("NFD", unicode(s)) if unicodedata.category(c) != "Mn"))


REGEXES = {
    ("AA", "3S"): [
        (ur"σε\(ν\)$", ur"σα"),
        (ur"([^σ])ε\(ν\)$", ur"\1ον"),
    ],

    ("AM", "3P"): [(ur"οντο$", ur"ομην")],

    ("AP", "3S"): [(ur"θη$", ur"θην")],

    ("FA", "2S"): [(ur"σεις$", ur"σω")],
    ("FA", "3S"): [(ur"σει$", ur"σω")],
    ("FA", "3P"): [(ur"σουσι\(ν\)$", ur"σω")],

    ("PA", "3S"): [(ur"^εστι\(ν\)$", ur"ειμι")],

    ("XA", "3S"): [(ur"ε\(ν\)$", ur"α")],
}

def calc_1s(form, tense_voice, person_number):
    results = set()
    for pattern, replacement in REGEXES.get((tense_voice, person_number), []):
        s = re.sub(pattern, replacement, form)
        if s != form:
            results.add(s)

    return results


for row in fs["sblgnt-lexemes"].rows():
    if row["ccat-pos"] == "V-":
        mood = row["ccat-parse"][3]
        if mood in "I":
            person_number = row["ccat-parse"][0] + row["ccat-parse"][5]
            tense_voice = row["ccat-parse"][1:3]
            if person_number == "1S":
                first_singular[row["lemma"]][tense_voice].add(strip_accents(row["norm"].decode("utf-8")))
        elif mood in "DSO":
            pass
        elif mood in "P":
            pass
        elif mood in "N":
            pass
        else:
            raise ValueError


match = 0
total = 0
first_fail = None


for row in fs["sblgnt-lexemes"].rows():
    if row["ccat-pos"] == "V-":
        mood = row["ccat-parse"][3]
        if mood in "I":
            person_number = row["ccat-parse"][0] + row["ccat-parse"][5]
            tense_voice = row["ccat-parse"][1:3]
            if first_singular[row["lemma"]][tense_voice]:
                total += 1
                calculated = calc_1s(strip_accents(row["norm"].decode("utf-8")), tense_voice, person_number)
                if calculated == first_singular[row["lemma"]][tense_voice]:
                    match += 1
                else:
                    if first_fail is None:
                        first_fail = (
                            row["norm"], tense_voice, person_number,
                            " ".join(first_singular[row["lemma"]][tense_voice]),
                            " ".join(calculated)
                        )
        elif mood in "DSO":
            pass
        elif mood in "P":
            pass
        elif mood in "N":
            pass
        else:
            raise ValueError

print "{}/{} = {}%".format(match, total, int(1000 * match / total) / 10)

if first_fail:
    print first_fail[0], first_fail[1], first_fail[2]
    print first_fail[3]
    print first_fail[4]
