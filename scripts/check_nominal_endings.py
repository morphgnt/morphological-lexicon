#!/usr/bin/env python3

DEBUG = False

from collections import defaultdict
import unicodedata


from morphgnt import filesets
from morphgnt.utils import load_wordset, collator, load_yaml, stemmer


lexemes = load_yaml("lexemes.yaml")

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


INDECLINABLE = load_wordset("nominal-indeclinable.txt")


# lemma -> person_number -> set of forms
forms = defaultdict(lambda: defaultdict(set))

fs = filesets.load("filesets.yaml")

for row in fs["sblgnt-lexemes"].rows():
    if row["lemma"] in INDECLINABLE:
        continue
    if row["ccat-pos"] in ["N-", "A-", "RA", "RD", "RI", "RP", "RR"]:
        case_number = row["ccat-parse"][4:6]
        if row["ccat-pos"] == "N-":
            key = row["lemma"]
        else:
            key = "{} ({}:{})".format(row["lemma"], row["ccat-parse"][6], row["ccat-parse"][7])
        forms[key][case_number].add(strip_accents(row["norm"]))
    elif row["ccat-pos"] == "V-" and row["ccat-parse"][3] == "P":
        case_number = row["ccat-parse"][4:6]
        key = "{} ({}:{})".format(row["lemma"], row["ccat-parse"][1:3], row["ccat-parse"][6])
        forms[key][case_number].add(strip_accents(row["norm"]))


# list of dicts mapping person_number to ending (or ?)
ENDINGS = []

NUMBERS = set()

# line num -> set of line num
MUTUAL = defaultdict(set)

FAILS = []

with open("nominal-endings.txt") as f:
    num = 0
    for line in f:
        num += 1
        line = line.split("#")[0].strip()
        if not line:
            continue
        endings = dict(zip(["NS", "GS", "AS", "DS", "VS", "NP", "GP", "AP", "DP", "VP", "line_num"], [i.strip() for i in line.split()] + [num]))
        NUMBERS.add(num)
        ENDINGS.append(endings)

for i in NUMBERS:
    for j in NUMBERS:
        if i != j:
            MUTUAL[i].add(j)


for lemma in sorted(forms, key=collator.sort_key):
    if DEBUG: print()
    if DEBUG: print(lemma, forms[lemma])

    matches = []
    for ending in ENDINGS:
        if DEBUG: print("    checking against", ending)
        fail = False
        stem = None
        for case_number in ["NS", "GS", "AS", "DS", "VS", "NP", "GP", "AP", "DP", "VP"]:
            if DEBUG: print("        {} {} {}".format(case_number, forms[lemma][case_number], ending[case_number]))
            if not forms[lemma][case_number]:
                if DEBUG: print("        skip")
                continue
            form_list = sorted(forms[lemma][case_number])
            ending_list = sorted(ending[case_number].split("/"))
            if len(form_list) != len(ending_list):
                if DEBUG: print("        different lengths")
                fail = True
                break
            for form, end in zip(form_list, ending_list):
                if DEBUG: print("            {} {}".format(form, end))
                proposed_stem = stemmer(form, end)
                if proposed_stem is None:
                    if DEBUG: print("        no match")
                    fail = True
                    break
                else:
                    if DEBUG: print("        proposed stem {}".format(proposed_stem))
                    if not stem:
                        stem = proposed_stem
                    if stem == proposed_stem:
                        if DEBUG: print("        {} == {}".format(stem, proposed_stem))
                    else:
                        if DEBUG: print("        stem failed")
                        fail = True
                        break
            if fail:
                break
        if fail or stem is None:
            if DEBUG: print("    failed")
        else:
            if DEBUG: print("    line {} matched with stem {}".format(ending["line_num"], stem))
            matches.append((ending["line_num"], stem))
            if ending["line_num"] in NUMBERS:
                NUMBERS.remove(ending["line_num"])
    # print("RESULT {} {}".format(matches, lemma))
    if not matches:
        FAILS.append(lemma)
    matched_lines = [num for num, stem in matches]
    for i in MUTUAL:
        to_remove = set()
        for j in MUTUAL[i]:
            if i in matched_lines and not j in matched_lines:
                to_remove.add(j)
        for j in to_remove:
            MUTUAL[i].remove(j)

print()
print("unused line numbers {}".format(sorted(NUMBERS)))

print()
for fail in FAILS:
    if fail.split()[0] in lexemes:
        morphcat = lexemes[fail.split()[0]].get("mounce-morphcat")
    else:
        morphcat = None
    print("{} {}: {}".format(fail, morphcat, dict(forms[fail])))
if FAILS:
    print("{} fails".format(len(FAILS)))

print()
for i in MUTUAL:
    if MUTUAL[i]:
        print("{} < {}".format(i, MUTUAL[i]))
