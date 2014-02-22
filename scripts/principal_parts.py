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
    ("AA", "1S"): [
        (ur"σα$", ur"σα"),
        (ur"ξα$", ur"ξα"),
        (ur"ον$", ur"ον"),
        (ur"ων$", ur"ων"),
        (ur"ον$", ur"α"),
        (ur"κα$", ur"κα"),
    ],
    ("AA", "2S"): [
        (ur"σας$", ur"σα"),
        (ur"ψας$", ur"ψα"),
        (ur"ες$", ur"ον"),
        (ur"ρας$", ur"ρα")
    ],
    ("AA", "3S"): [
        (ur"σε\(ν\)$", ur"σα"),
        (ur"([^σ])ε\(ν\)$", ur"\1ον"),
        (ur"([^σ])ε\(ν\)$", ur"\1α"),
        (ur"η$", ur"ην"),
        (ur"^ἐκραξε\(ν\)$", ur"ἐκεκραξα") # @@@
    ],
    ("AA", "1P"): [
        (ur"ομεν$", ur"ον"),
        (ur"ηκαμεν$", ur"ηκα"),
        (ur"ησαμεν$", ur"ησα"),
    ],
    ("AA", "2P"): [
        (ur"σατε$", ur"σα"),
        (ur"ετε$", ur"ον"),
        (ur"ατε$", ur"ον"),
        (ur"κατε$", ur"κα"),
    ],
    ("AA", "3P"): [
        (ur"αν$", ur"α"),
        (ur"αν$", ur"ον"),
        (ur"ον$", ur"ον"),
        (ur"ον$", ur"α"),
        (ur"ωσαν$", ur"ων"),
        (ur"ησαν$", ur"ην"),
        (ur"^ἐκραξαν$", ur"ἐκεκραξα"), # @@@
    ],

    #
    #
    ("AM", "3S"): [
        (ur"ετο$", ur"ομην"),
        (ur"ατο$", ur"αμην"),
    ],
    #
    #
    ("AM", "3P"): [(ur"οντο$", ur"ομην")],

    ("AP", "1S"): [(ur"ην$", ur"ην")],
    #
    ("AP", "3S"): [(ur"θη$", ur"θην")],
    ("AP", "1P"): [(ur"θημεν$", ur"θην")],
    #
    ("AP", "3P"): [(ur"ησαν$", ur"ην")],

    ("FA", "1S"): [
        (ur"σω$", ur"σω"),
        (ur"ξω$", ur"ξω"),
        (ur"ψω$", ur"ψω"),
        (ur"ρω$", ur"ρω"),
    ],
    ("FA", "2S"): [
        (ur"σεις$", ur"σω"),
        (ur"ρεις$", ur"ρω"),
    ],
    ("FA", "3S"): [
        (ur"σει$", ur"σω"),
        (ur"ξει$", ur"ξω"),
        (ur"εσει$", ur"ω"),
        (ur"ρει$", ur"ρω"),
        (ur"λει$", ur"λω"),
    ],
    #
    ("FA", "2P"): [
        (ur"σετε$", ur"σω"),
        (ur"ρειτε$", ur"ρω"),
    ],
    ("FA", "3P"): [
        (ur"σουσι\(ν\)$", ur"σω"),
        (ur"ξουσι\(ν\)$", ur"ξω"),
        (ur"ρουσι\(ν\)$", ur"ρω"),
        (ur"ουσι\(ν\)$", ur"ω")
    ],

    ("FM", "1S"): [
        (ur"σομαι$", ur"σομαι"),
        (ur"ξομαι$", ur"ξομαι"),
    ],
    #
    ("FM", "3S"): [
        (ur"σεται$", ur"σομαι"),
        (ur"^ἐσται$", ur"ἐσομαι")
    ],
    #
    ("FM", "2P"): [
        (ur"σεσθε$", ur"σομαι"),
    ],
    ("FM", "3P"): [
        (ur"σονται$", ur"σομαι"),
        (ur"ψονται$", ur"ψομαι"),
    ],

    ("FP", "1S"): [(ur"θησομαι$", ur"θησομαι")],
    #
    ("FP", "3S"): [(ur"θησεται$", ur"θησομαι")],
    #
    #
    #

    #
    #
    ("IA", "3S"): [
        (ur"ε\(ν\)$", ur"ον"),
        (ur"ει$", ur"ουν") # @@@ should this be a movable-nu in 3S?
    ],
    #
    #
    ("IA", "3P"): [(ur"ον$", ur"ον")],

    ("IM", "1P"): [(ur"μεθα$", ur"μην")],

    ("PA", "1S"): [
        (ur"ω$", ur"ω"),
        (ur"εἰμι$", ur"εἰμι"),
    ],
    ("PA", "2S"): [
        (ur"εις$", ur"ω"),
        (ur"ᾳς$", ur"ω"),
        (ur"^εἰ$", ur"εἰμι"),
    ],
    ("PA", "3S"): [
        (ur"ει$", ur"ω"),
        (ur"σι\(ν\)$", ur"μι"),
        (ur"ᾳ$", ur"ω"),
        (ur"^ἐστι\(ν\)$", ur"εἰμι"),
    ],
    ("PA", "1P"): [(ur"ομεν$", ur"ω")],
    ("PA", "2P"): [
        (ur"ετε$", ur"ω"),
        (ur"ετε$", ur"ημι"),
        (ur"ειτε$", ur"ω"),
        (ur"ουτε$", ur"ω"),
        (ur"^ἐστε$", ur"εἰμι"),
    ],
    ("PA", "3P"): [
        (ur"ουσι\(ν\)$", ur"ω"),
        (ur"ιωσι\(ν\)$", ur"ιω"),
        (ur"σι\(ν\)$", ur"μι"),
        (ur"εασι\(ν\)$", ur"ημι"),
    ],

    ("PM", "1S"): [(ur"μαι$", ur"μαι")],
    ("PM", "2S"): [
        (ur"ῃ$", ur"ομαι"),
        (ur"σαι$", ur"μαι"),
    ],
    ("PM", "3S"): [
        (ur"ται$", ur"μαι"),
        (ur"εται$", ur"ομαι"),
    ],
    ("PM", "1P"): [(ur"μεθα$", ur"μαι")],
    ("PM", "2P"): [
        (ur"σθε$", ur"μαι"),
        (ur"εισθε$", ur"ουμαι"),
    ],
    ("PM", "3P"): [
        (ur"νται$", ur"μαι"),
    ],

    #
    #
    #
    #
    #
    ("PP", "3P"): [(ur"ονται$", ur"ομαι")],

    ("XA", "1S"): [(ur"κα$", ur"κα")],
    ("XA", "2S"): [(ur"^οἰδας$", ur"οἰδα")],
    ("XA", "3S"): [(ur"ε\(ν\)$", ur"α")],
    ("XA", "1P"): [
        (ur"^οἰδαμεν$", ur"οἰδα")
    ],
    ("XA", "2P"): [
        (ur"κατε$", ur"κα"),
        (ur"^οἰδατε$", ur"οἰδα"),
    ],
    ("XA", "3P"): [(ur"κασι\(ν\)$", ur"κα")],
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
