#!/usr/bin/env python
# coding: utf-8


from collections import defaultdict
import re
import unicodedata

from morphgnt import filesets

fs = filesets.load("filesets.yaml")

first_singular = defaultdict(lambda: defaultdict(set))


ACUTE = u"\u0301"
GRAVE = u"\u0300"
CIRCUMFLEX = u"\u0342"


def strip_accents(w):
    return "".join(
        unicodedata.normalize("NFC", "".join(
            component for component in unicodedata.normalize("NFD", ch) if component not in [ACUTE, GRAVE, CIRCUMFLEX]
        )) for ch in w
    )


REGEXES = {
    ("AA", "1S"): [(ur"σα", ur"σα")],
    ("AA", "3S"): [
        (ur"σε\(ν\)$", ur"σα"),
        (ur"([^σ])ε\(ν\)$", ur"\1ον"),
        (ur"([^σ])ε\(ν\)$", ur"\1α"),
    ],
    ("AA", "1P"): [(ur"ομεν", ur"ον")],
    ("AA", "3P"): [
        (ur"αν$", ur"α"),
        (ur"αν$", ur"ον"),
        (ur"ον$", ur"ον"),
    ],

    ("AM", "3P"): [(ur"οντο$", ur"ομην")],

    ("AP", "3S"): [(ur"θη$", ur"θην")],
    ("AP", "3P"): [(ur"ησαν$", ur"ην")],

    ("FA", "2S"): [(ur"σεις$", ur"σω")],
    ("FA", "3S"): [
        (ur"σει$", ur"σω"),
        (ur"ξει$", ur"ξω"),
    ],
    ("FA", "3P"): [(ur"σουσι\(ν\)$", ur"σω")],

    ("IA", "3S"): [(ur"ε\(ν\)$", ur"ον")],

    ("PA", "1S"): [
        (ur"ω$", ur"ω"),
        (ur"εἰμι$", ur"εἰμι"),
    ],
    ("PA", "2S"): [(ur"^εἰ$", ur"εἰμι")],
    ("PA", "3S"): [
        (ur"ει$", ur"ω"),
        (ur"^ἐστι\(ν\)$", ur"εἰμι"),
    ],
    ("PA", "1P"): [(ur"ομεν$", ur"ω")],
    ("PA", "3P"): [
        (ur"σι\(ν\)", ur"μι"),
    ],

    ("PM", "2S"): [(ur"ῃ$", ur"ομαι")],
    ("PM", "3S"): [(ur"ται$", ur"μαι")],

    ("XA", "3S"): [(ur"ε\(ν\)$", ur"α")],
}

def calc_1s(form, tense_voice, person_number):
    results = set()
    for pattern, replacement in REGEXES.get((tense_voice, person_number), []):
        if re.search(pattern, form):
            s = re.sub(pattern, replacement, form)
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
                matched = True
                for option in first_singular[row["lemma"]][tense_voice]:
                    if option not in calculated:
                        matched = False
                if matched:
                    match += 1
                else:
                    if first_fail is None:
                        first_fail = (
                            strip_accents(row["norm"].decode("utf-8")).encode("utf-8"), tense_voice, person_number,
                            strip_accents(" ".join(first_singular[row["lemma"]][tense_voice])).encode("utf-8"),
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
    print "(\"{1}\", \"{2}\"): [(ur\"{0}$\", ur\"{3}\")],".format(*first_fail)
