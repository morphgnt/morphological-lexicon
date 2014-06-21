#!/usr/bin/env python3

import re
import unicodedata

ACUTE = "\u0301"
GRAVE = "\u0300"
CIRCUMFLEX = "\u0342"
SMOOTH = "\u0313"
ROUGH = "\u0314"


def strip_accents(w):
    return "".join(
        unicodedata.normalize("NFC", "".join(
            component
            for component in unicodedata.normalize("NFD", ch)
            if component not in [ACUTE, GRAVE, CIRCUMFLEX, SMOOTH, ROUGH]
        )) for ch in w
    )


REGEXES = [
    (r"(.*)ματα$", [
        (r"n-3c\(4\)$", r"APN:NPN$"),  # {54}
    ]),
    (r"(.*)(?<!ματ)α$", [
        (r"n-1[ach]$", r"NSF$"),  # {132, 133, 135, 139}
        (r"n-1e$", r"GSM$"),  # {111}
        (r"n-2[cd]$", r"APN:NPN$"),  # {47, 48}
        (r"n-3c\(6[abc]\)$", r"APN:NPN$"),  # {56} -τα
        (r"n-3c\(4\)$", r"ASN:NSN$"),  # {20} -μα
        (r"n-3", r"AS[FM]$"),  # (rest) {12, 13, 14, 15, 16, 17, 18, 21, 29,
                               #         32, 33, 34, 36, 37}
    ]),
    (r"(.*)τας$", [
        (r"n-1[bcfh]$", r"AP[FM]$"),  # {40, 41, 43, 44}
        (r"n-3", r"AP[FM]$"),  # (rest) {49, 50, 51, 52, 53, 58, 59, 62, 63,
                               #         64, 65, 66, 67}
    ]),
    (r"(.*)δας$", [
        (r"n-3c\(2\)$", r"AP[FM]$"),  # @@@
        (r"n-1[bcfh]$", r"AP[FM]$"),  # {40, 41, 43, 44}
        (r"n-1e$", r"NSM$"),  # {136}
    ]),
    (r"(.*)ας$", [
        (r"n-1e$", r"NSM$"),  # {136}
        (r"n-3c\([12]\)$", r"NS[FM]$"),  # {143}
        (r"n-1a$", r"APF:GSF$"),  # {38, 39}
        (r"n-1[bcfh]$", r"AP[FM]$"),  # {40, 41, 43, 44}
        (r"n-1d$", r"APM:NSM$"),  # {42}
        (r"n-3c\(6a\)$", r"ASN:NSN$"),  # {22}
        (r"n-3", r"AP[FM]$"),  # (rest) {49, 50, 51, 52, 53, 58, 59, 62, 63,
                               #         64, 65, 66, 67}
    ]),
    (r"(.*)ες$", [
        (r"(.*)$", r"NP[FM]$"),  # {156, 157, 158, 159, 160, 161, 162, 163,
                                 #  164, 165, 166, 167, 168, 169}
    ]),
    (r"(.*)ης$", [
        (r"n-1[bch]$", r"GSF$"),  # {109}
        (r"n-1f$", r"NSM$"),  # {137}
        (r"n-3", r"NS[FM]$"),  # {143, 144, 146}
    ]),
    (r"(.*)αις$", [
        (r"(.*)$", r"DP.$"),  # {96}
    ]),
    (r"(.*)οις$", [
        (r"(.*)$", r"DP.$"),  # {97}
    ]),
    (r"(.*)εις$", [
        (r"(.*)$", r"AP([FM]):NP\1$"),  # {60, 61}
    ]),
    (r"(.*)[^αοε]ις$", [
        (r"(.*)$", r"NS[FM]$"),  # {143, 150}
    ]),
    (r"(.*)ος$", [
        (r"n-2[ab]$", r"NS[FM]$"),  # 140
        (r"n-3d\(2b\)$", r"ASN:NSN$"),  # {26}
        (r"n-3", r"GS.$"),  # {113, 114, 115, 116, 117, 118, 119, 120, 122, 124
                            #  126, 127, 128, 129, 130}
    ]),
    (r"((.*)[^εο])?υς$", [
        (r"(.*)$", r"NS[FM]$"),  # {147, 153}
    ]),
    (r"(.*)ευς$", [
        (r"(.*)$", r"NSM$"),  # {148} n-3e(3)
    ]),
    (r"(.*)ους$", [
        (r"n-3c\(6c\)$",  r"ASN:NSN$"),  # {24}
        (r"n-2[ab]$", r"AP[FM]$"),  # {45, 46}
        (r"n-3d\((2b|3)\)$", r"GS[FN]$"),  # {121}
        (r"n-3c\([12]\)$", r"NS[FM]$"),  # {143}
        (r"n-3e\(4\)$", r"NSM$"),  # {149}
    ]),
    (r"(.*)[^ε]ως$", [
        (r"n-3c\(6c\)$", r"ASN:NSN$"),  # {24} φῶς
        (r"n-3c\([12]\)$", r"NSM$"),  # {143} ἱδρώς|γέλως
    ]),
    (r"(.*)εως$", [
        (r"(.*)$", r"GS.$"),  # {123, 125}
    ]),
    (r"(.*)αν$", [
        (r"(.*)$", r"AS[FM]$"),  # {0, 1, 3, 4, 5, 7}
    ]),
    (r"(.*)ην$", [
        (r"n-1[bfh]$", r"AS[FM]$"),  # {2, 6, 7}
        (r"n-3d\(2a\)$", r"ASM$"),  # {25}
        (r"n-3f\(1.\)$", r"NS[FM]$"),  # {151}
    ]),
    (r"(.*)[^σξ]ιν$", [
        (r"n-3f\(1a\)$", r"NSF$"),  # {151} ὠδίν
        (r"n-3", r"AS[FM]$"),  # {19, 31}
    ]),
    (r"(.*)ξιν$", [
        (r"n-3e\(5b\)$", r"AS[FM]$"),  # {31} fall-through
        (r"n-3b\([1-3]\)$", r"DPF$"),  # {98}
    ]),
    (r"(.*)εσιν$", [
        (r"n-3e\(5b1\)$", r"AS[FM]$"),  # @@@
        (r"(.*)$", r"DP.$"),  # @@@
    ]),
    (r"(.*)σιν$", [
        (r"n-3e\(5b\)$", r"AS[FM]$"),  # {31} fall-through
        (r"(.*)$", r"DP.$"),  # {99, 100, 101, 102, 103, 104, 105, 106, 107,
                              #  108}
    ]),
    (r"(.*)ον$", [
        (r"n-2[ab]$", r"AS[FM]$"),  # {8, 9}
        (r"n-2c$", r"ASN:NSN$"),  # {10}
    ]),
    (r"(.*)ουν$", [
        (r"n-2d$", r"ASN:NSN$"),  # {11}
        (r"n-3", r"ASM$"),  # {30}
    ]),
    (r"(.*)[^ο]υν$", [
        (r"(.*)$", r"AS[FM]$"),  # {27, 28}
    ]),
    (r"(.*)(ιν|εν|ον|ην|ων|οντ)ων$", [
        (r"(.*)$", r"GP.$"),  # {131}
    ]),
    (r"(.*)ων$", [
        (r"n-3c\(5b\)$", r"NSM$"),  # {145}
        (r"n-3f\(1.\)", r"NS[FM]$"),  # {151}
        (r"(.*)$", r"GP.$"),  # {131}
    ]),
    (r"(.*)αι$", [
        (r"(.*)$", r"NP[FM]$"),  # {154}
    ]),
    (r"(.*)οι$", [
        (r"(.*)$", r"NP[FM]$"),  # {155}
    ]),
    (r"(.*)σι$", [
        (r"(.*)$", r"DP.$"),  # {99, 100, 101, 102, 103, 104, 105, 106, 107,
                              #  108}
    ]),
    (r"(.*)ξι$", [
        (r"(.*)$", r"DPF$"),  # {98}
    ]),
    (r"(.*)[^αοσξ]ι$", [
        (r"(.*)$", r"DS.$"),  # {77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 88,
                              #  90, 91, 92, 93, 94, 95}
    ]),
    (r"(.*)ϊ$", [
        (r"(.*)$", r"DS[FM]$"),  # {87, 89}
    ]),
    (r"(.*)ρ$", [
        (r"n-3f\(2.\)$", r"NS[FM]$"),  # {152}
        (r"(.*)$", r"ASN:NSN$"),  # {23, 35}
    ]),
    (r"(.*)ξ$", [
        (r"(.*)$", r"NS[FM]$"),  # {142, 143}
    ]),
    (r"(.*)ψ$", [
        (r"(.*)$", r"NS[FM]$"),  # {141}
    ]),
    (r"(.*)ου$", [
        (r"(.*)$", r"GS.$"),  # {110, 112}
    ]),
    (r"(.*)η$", [
        (r"n-1", r"NSF$"),  # {134, 138}
        (r"n-3", r"APN:NPN$"),  # {57}
    ]),
    (r"(.*)ᾳ$", [
        (r"(.*)$", r"DS[FM]$"),  # {68, 69, 72, 73}
    ]),
    (r"(.*)ῃ$", [
        (r"(.*)$", r"DS[FM]$"),  # {70, 71, 74, 75}
    ]),
    (r"(.*)ῳ$", [
        (r"(.*)$", r"DS.$"),  # {76}
    ]),
]


fail_count = 0
with open("noun_forms_1.txt") as f:
    for line in f:
        form1, mounce, parses, count = line.strip().split("|")

        if not mounce.startswith("n-"):
            continue

        if form1.endswith("(ν)"):
            options = [form1[:-3], form1[:-3] + "ν"]
        else:
            options = [form1]

        for form in options:
            form_match = None
            for i, res in enumerate(REGEXES):
                form_re, solutions = res
                if re.match(form_re, strip_accents(form)):
                    form_match = form_re
                    solution_match = None
                    for mounce_re, parse_re in solutions:
                        if re.match(mounce_re, mounce):
                            if re.match(parse_re, parses):
                                solution_match = mounce_re
                            break
                    break

            if solution_match and form_match:
                form_match = form_match.replace("(.*)", "-").strip("$")
                print(form, mounce, parses, count, form_match, solution_match)
            else:
                fail_count += 1

                if fail_count == 1:
                    print(parses, mounce, form, form1)

if fail_count:
    print("{} fails".format(fail_count))
