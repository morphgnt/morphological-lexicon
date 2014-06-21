#!/usr/bin/env python3

from collections import defaultdict
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


# lemma -> pos_gender_degree -> person_number -> set of forms
forms = defaultdict(lambda: defaultdict(lambda: defaultdict(set)))

fs = filesets.load("filesets.yaml")

for row in fs["sblgnt-lexemes"].rows():
    if row["ccat-pos"] in ["N-", "A-", "RA", "RD", "RI", "RP", "RR"]:
        pos_gender_degree = row["ccat-pos"] + ":" + row["ccat-parse"][6] + ":" + row["ccat-parse"][7]
        case_number = row["ccat-parse"][4:6]
        forms[row["lemma"]][pos_gender_degree][case_number].add(strip_accents(row["norm"]))


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
    return tuple(
        ("/".join(i[offset - 1:] for i in d[case_number]) if case_number in d else "?")
        for case_number in ["NS", "GS", "AS", "DS", "VS", "NP", "GP", "AP", "DP", "VP"]
    )

# pos_gender_degree -> ending_tuple -> set of lemmas
endings = defaultdict(lambda: defaultdict(set))

for lemma in forms:
    for pos_gender_degree in forms[lemma]:
        t = to_tuple(forms[lemma][pos_gender_degree])
        if t:
            endings[pos_gender_degree][t].add(lemma)


for pos_gender_degree in endings:
    for t in endings[pos_gender_degree]:
        print(pos_gender_degree, "\t".join(t), end="\t")
        print(", ".join(endings[pos_gender_degree][t]))

