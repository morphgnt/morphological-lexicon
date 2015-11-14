#!/usr/bin/env python3

from collections import defaultdict

from characters import strip_accents, strip_breathing

CELLS = defaultdict(lambda: defaultdict(set))
GENDER = defaultdict(set)
LEMMAS = defaultdict(set)

with open("nominals.txt") as f:
    for line in f:
        lemma, mounce1, aspect_voice, gender, mounce2, theme1, case_number, norm, theme2, distinguisher, explanation = line.strip().split()

        CELLS[mounce2][case_number + gender].add((strip_breathing(strip_accents(distinguisher)), explanation))
        GENDER[mounce2].add(gender)
        LEMMAS[mounce2 + " " + gender].add(lemma)


for mounce in sorted(CELLS, key=lambda x: x[0] + x[2:]):
    for gender in ["M", "F", "N", "-"]:
        if gender in GENDER[mounce]:
            print("\n\n{} {} ({}):".format(mounce, gender, len(LEMMAS[mounce + " "+ gender])))
            for case_number in ["NS", "GS", "DS", "AS", "VS", "NP", "VP", "GP", "DP", "AP"]:
                if case_number + gender in CELLS[mounce]:
                    if len(CELLS[mounce][case_number + gender]) == 1:
                        cell = CELLS[mounce][case_number + gender].pop()
                        print("    {}:   {:10} {{{}}}".format(case_number, cell[0], cell[1]))
                    else:
                        print("    {}:".format(case_number))
                        for cell in CELLS[mounce][case_number + gender]:
                            print("        - {:10} {{{}}}".format(cell[0], cell[1]))
