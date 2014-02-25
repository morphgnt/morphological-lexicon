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
        (ur"ψα$", ur"ψα"),
        (ur"ρα$", ur"ρα"),
        (ur"κα$", ur"κα"),
        (ur"ον$", ur"ον"),
        (ur"ον$", ur"α"),
        (ur"ων$", ur"ων"),
        (ur"α$", ur"ον"),
        (ur"α$", ur"α"),
        (ur"ην$", ur"ην"),
    ],
    ("AA", "2S"): [
        (ur"σας$", ur"σα"),
        (ur"ψας$", ur"ψα"),
        (ur"ες$", ur"ον"),
        (ur"ρας$", ur"ρα"),
        (ur"κας$", ur"κα"),
        (ur"ας$", ur"ον"),
        (ur"ας$", ur"α"),
        (ur"ες$", ur"ον"),
        (ur"ες$", ur"α"),
        (ur"ως$", ur"ων"),
    ],
    ("AA", "3S"): [
        (ur"σε\(ν\)$", ur"σα"),
        (ur"([^σ])ε\(ν\)$", ur"\1ον"),
        (ur"([^σ])ε\(ν\)$", ur"\1α"),
        (ur"αμησε\(ν\)$", ur"ημα"),
        (ur"η$", ur"ην"),
        (ur"ω$", ur"ων"),
        (ur"^κατελειπε\(ν\)$", ur"κατελιπον"),
        (ur"^ηὐδοκησε\(ν\)$", ur"εὐδοκησα"),
        (ur"^ἐκραξε\(ν\)$", ur"ἐκεκραξα"), # @@@
    ],
    ("AA", "1P"): [
        (ur"σαμεν$", ur"σα"),
        (ur"ξαμεν$", ur"ξα"),
        (ur"ψαμεν$", ur"ψα"),
        (ur"καμεν$", ur"κα"),
        (ur"λαμεν$", ur"λα"),
        (ur"ναμεν$", ur"να"),
        (ur"ραμεν$", ur"ρα"),
        (ur"ομεν$", ur"ον"),
        (ur"αμεν$", ur"ον"),
    ],
    ("AA", "2P"): [
        (ur"σατε$", ur"σα"),
        (ur"ετε$", ur"ον"),
        (ur"ατε$", ur"ον"),
        (ur"ατε$", ur"α"),
        (ur"κατε$", ur"κα"),
    ],
    ("AA", "3P"): [
        (ur"αν$", ur"α"),
        (ur"αν$", ur"ον"),
        (ur"ον$", ur"ον"),
        (ur"ον$", ur"α"),
        (ur"ωσαν$", ur"ων"),
        (ur"ησαν$", ur"ην"),
        (ur"οσαν$", ur"ωκα"),
        (ur"οσαν$", ur"ον"),
        (ur"^ἐκραξαν$", ur"ἐκεκραξα"), # @@@
    ],

    ("AM", "1S"): [
        (ur"σαμην$", ur"σαμην"),
        (ur"ξαμην$", ur"ξαμην"),
        (ur"ψαμην$", ur"ψαμην"),
        (ur"λαμην$", ur"λαμην"),
        (ur"ομην$", ur"ομην"),
        (ur"εμην$", ur"εμην"),
        (ur"([^μ])ην$", ur"\1ην"),
    ],
    ("AM", "2S"): [
        (ur"ου$", ur"ομην"),
        (ur"ξω$", ur"ξαμην"),
    ],
    ("AM", "3S"): [
        (ur"ετο$", ur"ομην"),
        (ur"ατο$", ur"αμην"),
        (ur"ετο$", ur"εμην"),
    ],
    ("AM", "1P"): [(ur"σαμεθα$", ur"σαμην")],
    ("AM", "2P"): [
        (ur"εσθε$", ur"ομην"),
        (ur"ξασθε$", ur"ξαμην"),
    ],
    ("AM", "3P"): [
        (ur"οντο$", ur"ομην"),
        (ur"σαντο$", ur"σαμην"),
        (ur"ξαντο$", ur"ξαμην"),
        (ur"θεντο$", ur"θεμην"),
    ],

    ("AP", "1S"): [(ur"ην$", ur"ην")],
    ("AP", "2S"): [(ur"θης$", ur"θην")],
    ("AP", "3S"): [
        (ur"θη$", ur"θην"),
        (ur"λη$", ur"λην"),
        (ur"ρη$", ur"ρην"),
    ],
    ("AP", "1P"): [
        (ur"θημεν$", ur"θην"),
        (ur"ρημεν$", ur"ρην"),
    ],
    ("AP", "2P"): [
        (ur"θητε$", ur"θην"),
        (ur"ρητε$", ur"ρην"),
    ],
    ("AP", "3P"): [(ur"ησαν$", ur"ην")],

    ("FA", "1S"): [
        (ur"σω$", ur"σω"),
        (ur"ξω$", ur"ξω"),
        (ur"ψω$", ur"ψω"),
        (ur"ρω$", ur"ρω"),
        (ur"λω$", ur"λω"),
        (ur"νω$", ur"νω"),
        (ur"εω$", ur"εω"),
        (ur"ιω$", ur"ιω"),
    ],
    ("FA", "2S"): [
        (ur"σεις$", ur"σω"),
        (ur"ρεις$", ur"ρω"),
    ],
    ("FA", "3S"): [
        (ur"σει$", ur"σω"),
        (ur"ξει$", ur"ξω"),
        (ur"ψει$", ur"ψω"),
        (ur"εσει$", ur"ω"),
        (ur"ρει$", ur"ρω"),
        (ur"λει$", ur"λω"),
        (ur"νει$", ur"νω"),
    ],
    ("FA", "1P"): [
        (ur"σομεν$", ur"σω"),
        (ur"ξομεν$", ur"ξω"),
        (ur"ρουμεν$", ur"ρω"),
        (ur"νουμεν$", ur"νω"),
    ],
    ("FA", "2P"): [
        (ur"σετε$", ur"σω"),
        (ur"ειτε$", ur"ω")
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
        (ur"ψομαι$", ur"ψομαι"),
    ],
    ("FM", "2S"): [
        (ur"σῃ$", ur"σομαι"),
        (ur"ψῃ$", ur"ψομαι"),
    ],
    ("FM", "3S"): [
        (ur"σεται$", ur"σομαι"),
        (ur"ψεται$", ur"ψομαι"),
        (ur"^ἐσται$", ur"ἐσομαι")
    ],
    ("FM", "1P"): [
        (ur"σομεθα$", ur"σομαι"),
        (ur"ψομεθα$", ur"ψομαι"),
    ],
    ("FM", "2P"): [
        (ur"σεσθε$", ur"σομαι"),
        (ur"ψεσθε$", ur"ψομαι")
    ],
    ("FM", "3P"): [
        (ur"σονται$", ur"σομαι"),
        (ur"ξονται$", ur"ξομαι"),
        (ur"ψονται$", ur"ψομαι"),
    ],

    ("FP", "1S"): [
        (ur"θησομαι$", ur"θησομαι"),
        (ur"ρησομαι$", ur"ρησομαι"),
    ],
    ("FP", "2S"): [(ur"θησῃ$", ur"θησομαι")],
    ("FP", "3S"): [
        (ur"ρησεται$", ur"ρησομαι"),
        (ur"θησεται$", ur"θησομαι"),
    ],
    ("FP", "1P"): [(ur"θησομεθα$", ur"θησομαι")],
    ("FP", "2P"): [(ur"θησεσθε$", ur"θησομαι")],
    ("FP", "3P"): [
        (ur"θησονται$", ur"θησομαι"),
        (ur"ρησονται$", ur"ρησομαι"),
    ],

    ("IA", "1S"): [
        (ur"ουν$", ur"ουν"),
        (ur"ον$", ur"ον"),
        (ur"ων$", ur"ων"),
    ],
    ("IA", "2S"): [(ur"ες$", ur"ον")],
    ("IA", "3S"): [
        (ur"ε\(ν\)$", ur"ον"),
        (ur"^ἐμελλε\(ν\)$", ur"ἠμελλον"),
        (ur"ει$", ur"ουν") # @@@ should this be a movable-nu in 3S?
    ],
    ("IA", "1P"): [
        (ur"ομεν$", ur"ον"),
        (ur"ουμεν$", ur"ουν"),
    ],
    ("IA", "2P"): [
        (ur"ετε$", ur"ον"),
        (ur"ειτε$", ur"ουν"),
        (ur"ητε$", ur"ων"),
    ],
    ("IA", "3P"): [
        (ur"ον$", ur"ον"),
        (ur"ουν$", ur"ουν"),
        (ur"οσαν$", ur"ον"),
        (ur"^ἐμελλον$", ur"ἠμελλον"),
    ],

    ("IM", "1S"): [(ur"μην$", ur"μην")],
    ("IM", "2S"): [(ur"ἠσθα$", ur"ἠμην")],
    ("IM", "3S"): [
        (ur"ετο$", ur"ομην"),
        (ur"ειτο$", ur"ουμην"),
    ],
    ("IM", "1P"): [(ur"μεθα$", ur"μην")],
    # 1
    ("IM", "3P"): [
        (ur"οντο$", ur"ομην"),
        (ur"ουντο$", ur"ουμην"),
    ],

    ("IP", "1S"): [(ur"ομην$", ur"ομην")],
    # 2
    # 3
    # 4
    # 5
    # 6

    ("PA", "1S"): [
        (ur"ω$", ur"ω"),
        (ur"μι$", ur"μι"),
    ],
    ("PA", "2S"): [
        (ur"εις$", ur"ω"),
        (ur"ῃς$", ur"ω"),
        (ur"ᾳς$", ur"ω"),
        (ur"νυεις$", ur"νυμι"),
        (ur"εις$", ur"ιημι"),
        (ur"^εἰ$", ur"εἰμι"),
    ],
    ("PA", "3S"): [
        (ur"ει$", ur"ω"),
        (ur"ᾳ$", ur"ω"),
        (ur"ῃ$", ur"ω"),
        (ur"οι$", ur"ω"),
        (ur"σι\(ν\)$", ur"μι"),
        (ur"^ἐστι\(ν\)$", ur"εἰμι"),
    ],
    ("PA", "1P"): [
        (ur"ομεν$", ur"ω"),
        (ur"ουμεν$", ur"ω"),
        (ur"ωμεν$", ur"ω"),
        (ur"ομεν$", ur"ημι"),
        (ur"ιστανομεν$", ur"ιστημι"), # @@@
        (ur"^ἐσμεν$", ur"εἰμι"),
    ],
    ("PA", "2P"): [
        (ur"ετε$", ur"ω"),
        (ur"ετε$", ur"ημι"),
        (ur"ειτε$", ur"ω"),
        (ur"ουτε$", ur"ω"),
        (ur"ατε$", ur"ω"),
        (ur"ητε$", ur"ω"),
        (ur"^ἐστε$", ur"εἰμι"),
    ],
    ("PA", "3P"): [
        (ur"ουσι\(ν\)$", ur"ω"),
        (ur"ωσι\(ν\)$", ur"ω"),
        (ur"σι\(ν\)$", ur"μι"),
        (ur"εασι\(ν\)$", ur"ημι"),
        (ur"ασι\(ν\)$", ur"ημι"),
        (ur"ουσι\(ν\)$", ur"ημι"),
        (ur"οασι\(ν\)$", ur"ωμι"),
    ],

    ("PM", "1S"): [(ur"μαι$", ur"μαι")],
    ("PM", "2S"): [
        (ur"ῃ$", ur"ομαι"),
        (ur"ῃ$", ur"αμαι"),
        (ur"ῃ$", ur"ουμαι"),
        (ur"ῃ$", ur"ημαι"),
        (ur"σαι$", ur"μαι"),
        (ur"ασαι$", ur"ωμαι"),
        (ur"ει$", ur"ομαι"),
    ],
    ("PM", "3S"): [
        (ur"ται$", ur"μαι"),
        (ur"εται$", ur"ομαι"),
        (ur"ειται$", ur"ουμαι"),
    ],
    ("PM", "1P"): [(ur"μεθα$", ur"μαι")],
    ("PM", "2P"): [
        (ur"σθε$", ur"μαι"),
        (ur"εισθε$", ur"ουμαι"),
        (ur"εσθε$", ur"ομαι"),
        (ur"ασθε$", ur"ωμαι"),
    ],
    ("PM", "3P"): [
        (ur"νται$", ur"μαι"),
    ],

    ("PP", "1S"): [
        (ur"ομαι$", ur"ομαι"),
        (ur"ουμαι$", ur"ουμαι"),
        (ur"ειμαι$", ur"ειμαι"),
        (ur"ωμαι$", ur"ωμαι"),
    ],
    # 7
    ("PP", "3S"): [
        (ur"εται$", ur"ομαι"),
        (ur"ειται$", ur"ουμαι"),
        (ur"ειται$", ur"ειμαι"),
        (ur"νεται$", ur"νομαι"),
        (ur"ρεται$", ur"ρομαι"),
    ],
    ("PP", "1P"): [
        (ur"ομεθα$", ur"ομαι"),
        (ur"ουμεθα$", ur"ουμαι"),
    ],
    # 8
    ("PP", "3P"): [(ur"ονται$", ur"ομαι")],

    ("XA", "1S"): [
        (ur"κα$", ur"κα"),
        (ur"θα$", ur"θα"),
        (ur"φα$", ur"φα"),
        (ur"χα$", ur"χα"),
        (ur"να$", ur"να"),
        (ur"οιδα$", ur"οιδα"),
        (ur"^οἰδα$", ur"οἰδα"),
        (ur"^ἑορακα$", ur"ἑωρακα"),
        (ur"^ἑωρακα$", ur"ἑορακα"),
    ],
    ("XA", "2S"): [
        (ur"κας$", ur"κα"),
        (ur"νας$", ur"να"),
        (ur"θας$", ur"θα"),
        (ur"φας$", ur"φα"),
        (ur"κες$", ur"κα"),
        (ur"^οἰδας$", ur"οἰδα"),
        (ur"^ἑωρακας$", ur"ἑορακα"),
    ],
    ("XA", "3S"): [
        (ur"κε\(ν\)$", ur"κα"),
        (ur"([^κ])ε\(ν\)$", ur"\1α"),
        (ur"^ἑωρακε\(ν\)$", ur"ἑορακα"),
        (ur"^ἑορακε\(ν\)$", ur"ἑωρακα"),
    ],
    ("XA", "1P"): [
        (ur"καμεν$", ur"κα"),
        (ur"([^κ])αμεν$", ur"\1α"),
        (ur"^ἑωρακαμεν$", ur"ἑορακα"),
        (ur"^οἰδαμεν$", ur"οἰδα"),
    ],
    ("XA", "2P"): [
        (ur"κατε$", ur"κα"),
        (ur"([^κ])ατε$", ur"\1α"),
        (ur"^ἑωρακατε$", ur"ἑορακα"),
        (ur"^ἰστε$", ur"οἰδα"),
        (ur"^οἰδατε$", ur"οἰδα"),
    ],
    ("XA", "3P"): [
        (ur"κασι\(ν\)$", ur"κα"),
        (ur"νασι\(ν\)$", ur"να"),
        (ur"καν$", ur"κα"),
        (ur"([^κ])αν$", ur"\1α"),
        (ur"^ἑωρακαν$", ur"ἑορακα"),
        (ur"^ἑωρακασι\(ν\)$", ur"ἑορακα"),
        (ur"^ἑορακαν$", ur"ἑωρακα"),
        (ur"^οἰδασι\(ν\)$", ur"οἰδα"),
        (ur"^ἰσασι\(ν\)$", ur"οἰδα"),
    ],

    ("XM", "1S"): [
        (ur"αμαι$", ur"αμαι"),
        (ur"ημαι$", ur"ημαι"),
        (ur"ευμαι$", ur"ευμαι"),
        (ur"σμαι$", ur"σμαι"),
    ],
    # 9
    ("XM", "3S"): [
        (ur"ηται$", ur"ημαι"),
        (ur"σται$", ur"σμαι"),
        (ur"αται$", ur"αμαι"),
    ],
    ("XM", "1P"): [(ur"αμεθα$", ur"αμαι")],
    # 11
    # 12

    ("XP", "1S"): [(ur"μαι$", ur"μαι")],
    ("XP", "2S"): [(ur"σαι$", ur"μαι")],
    ("XP", "3S"): [(ur"ται$", ur"μαι")],
    ("XP", "1P"): [(ur"μεθα$", ur"μαι")],
    # 13
    # 14

    ("YA", "1S"): [(ur"ειν$", ur"ειν")],
    ("YA", "2S"): [(ur"εις$", ur"ειν")],
    ("YA", "3S"): [(ur"ει$", ur"ειν")],
    # 15
    ("YA", "2P"): [(ur"ειτε$", ur"ειν")],
    ("YA", "3P"): [(ur"εισαν$", ur"ειν")],
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
line_total = 0
line_fail = 0

for row in fs["sblgnt-lexemes"].rows():
    line_total += 1
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
                        line_fail = line_total
        elif mood in "DSO":
            pass
        elif mood in "P":
            pass
        elif mood in "N":
            pass
        else:
            raise ValueError

print "{}/{} = {}% [{}/{} = {}%]".format(match, total, int(1000 * match / total) / 10, line_fail, line_total, int(1000 * line_fail / line_total)/ 10)

if first_fail:
    print "(\"{1}\", \"{2}\"): [(ur\"{0}$\", ur\"{3}\")],".format(*first_fail)
