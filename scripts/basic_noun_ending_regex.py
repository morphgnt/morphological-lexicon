#!/usr/bin/env python3

import re
import sys
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


REGEX_TEMPLATES = {
    "EIR_α": r"(έα|εά|ια|ία|ΐα|ιά|ρα|ρά)",
    "EIR_α2": r"(έα|εά|εᾶ|ια|ία|ΐα|ιά|ιᾶ|ρα|ρά|ρᾶ)",
    "notEIR_α": r"([^έειίΐρ](α|ά))",

    "EIR_ᾳ": r"(εᾷ|έᾳ|ίᾳ|ΐᾳ|ιᾷ|ρᾳ|ρᾷ)",
    "notEIR_ᾳ": r"[^έειίΐρ](ᾳ|ᾷ)",

    "EO": r"(ε|έ|ο|ό)",
    "C": r"[βγδζθκλμνξπρστχψφ]",
    "V:": r"(α|ᾶ|ι|ί|ῖ|υ|ῦ|η|ή|ῆ|ω|ώ|ῶ|ει|εῖ)",
}


def r(regex):
    regex = re.sub("^-", "(.*)", regex)
    for name, substitution in REGEX_TEMPLATES.items():
        regex = re.sub("{{{}}}".format(name), substitution, regex)
    regex += "$"
    return regex


REGEXES = [

    # (r"AS[FM]$", r"n-1.", r("-(α|ά|ᾶ|η|ή|ῆ)ν")),
    # (r"AS[FM]|ASN:NSN$", r"n-2.", r("-(ο|ό|οῦ)ν")),

    ####

    ### accusative singular

    ## first-declension

    (r"ASF$",           r"n-1a",                r("-{EIR_α}ν")),
    (r"ASF$",           r"n-1a",                r("-{notEIR_α}ν")),
    (r"ASF$",           r"n-1b",                r("-(η|ή)ν")),
    (r"ASF$",           r"n-1c",                r("-αν")),
    (r"ASM$",           r"n-1d",                r("-{EIR_α}ν")),
    (r"ASM$",           r"n-1e",                r("-(α|ᾶ)ν")),
    (r"ASM$",           r"n-1f",                r("-(η|ή)ν")),
    (r"AS[FM]$",        r"n-1h",                r("-(ᾶ|ῆ)ν")),

    ## second declension

    (r"ASM$",           r"n-2a",                r("-(ον|όν)")),            # 8
    (r"ASF$",           r"n-2b",                r("-(ον|όν)")),
    (r"ASN:NSN$",       r"n-2c",                r("-(ον|όν)")),
    (r"ASN:NSN$",       r"n-2d",                r("-οῦν")),

    ## third declension (3a & 3b & 3c(1,2,3))

    (r"ASM$",           r"n-3a\(1\)",           r("-πα")),
    (r"ASM$",           r"n-3a\(2\)",           r("-βα")),                # 13
    (r"AS[FM]$",        r"n-3b\(1\)",           r("-κα")),
    (r"ASF$",           r"n-3b\(2\)",           r("-γα")),
    (r"ASF$",           r"n-3b\(3\)",           r("-χα")),
    (r"ASF$",           r"n-3c\(1\)",           r("-[^ν]τα")),
    (r"AS[FM]$",        r"n-3c\(2\)",           r("-δα")),

    # χάριν, προφῆτιν, (ἔριν, κλεῖν)
    (r"ASF$",           r"n-3c\([12]\)",        r("-(ι|ῖ)ν")),

    ## third declension (3c(4,5))

    (r"ASN:NSN$",       r"n-3c\(4\)",           r("-μα")),
    (r"ASM$",           r"n-3c\(5.\)",          r("-ντα")),

    ## third declension (3c(6))

    (r"ASN:NSN$",       r"n-3c\(6a\)",          r("-ας")),
    (r"ASN:NSN$",       r"n-3c\(6b\)",          r("-ρ")),                  # 23
    (r"ASN:NSN$",       r"n-3c\(6c\)",          r("-[^α]ς")),

    ## third declension (3d)

    (r"ASM$",           r"n-3d\(2a\)",          r("-ην$")),
    (r"ASN:NSN$",       r"n-3d\(2b\)",          r("-ος$")),

    ## third declension (3e(1-4))

    (r"AS[FM]$",        r"n-3e\(1\)",           r("-(υν|ύν)")),
    (r"ASF$",           r"n-3e\(2\)",           r("-αῦν")),
    (r"ASM$",           r"n-3e\(3\)",           r("-έα")),
    (r"ASM$",           r"n-3e\(4\)",           r("-οῦν")),

    ## third declension (3e(5-6))

    (r"AS[FM]$",        r"n-3e\(5b\)",          r("-ιν")),

    ## third declension (3f)

    (r"AS[FM]$",        r"n-3f\(1a\)",          r("-{V:}να")),             # 32
    (r"AS[FM]$",        r"n-3f\(1b\)",          r("-{EO}να")),
    (r"AS[FM]$",        r"n-3f\(2a\)",          r("-{V:}ρα")),
    (r"ASN:NSN$",       r"n-3f\(2a\)",          r("-{V:}ρ")),
    (r"ASM$",           r"n-3f\(2b\)",          r("-{EO}ρα")),
    (r"AS[FM]$",        r"n-3f\(2c\)",          r("-(έ)?ρα")),


    ### accusative plural

    ## first declension

    (r"APF:GSF$",       r"n-1a",                r("-{EIR_α2}ς")),
    (r"APF:GSF$",       r"n-1a",                r("-{notEIR_α}ς")),
    (r"APF$",           r"n-1b",                r("-(α|ά)ς")),
    (r"APF$",           r"n-1c",                r("-ας")),
    (r"APM:NSM$",       r"n-1d",                r("-{EIR_α}ς")),
    (r"APM$",           r"n-1f",                r("-(α|ά)ς")),
    (r"APF$",           r"n-1h",                r("-ᾶς")),

    ## second declension

    (r"APM$",           r"n-2a",                r("-(ους|ούς)")),
    (r"APF$",           r"n-2b",                r("-(ους|ούς)")),

    (r"APN:NPN$",       r"n-2c",                r("-(α|ά)")),
    (r"APN:NPN$",       r"n-2d",                r("-έα")),

    ## third declension (3a & 3b & 3c(1,2,3))

    (r"AP[FM]$",        r"n-3b\(1\)",           r("-κας")),
    (r"APF$",           r"n-3b\(2\)",           r("-γας")),
    (r"APF$",           r"n-3b\(3\)",           r("-χας")),

    (r"APF$",           r"n-3c\(1\)",           r("-τας")),
    (r"AP[FM]$",        r"n-3c\(2\)",           r("-δας")),

    ## third declension (3c(4,5))

    (r"APN:NPN$",       r"n-3c\(4\)",           r("-ματα")),
    (r"APM$",           r"n-3c\(5.\)",          r("-ντας")),

    ## third declension (3c(6))

    (r"APN:NPN$",       r"n-3c\(6[abc]\)",      r("-τα")),

    ## third declension (3d)

    (r"APN:NPN$",       r"n-3d\(2b\)",          r("-η")),

    ## third declension (3e(1-4))

    (r"AP[FM]$",        r"n-3e\(1\)",           r("-(υας|ύας)")),
    (r"APM$",           r"n-3e\(4\)",           r("-όας")),

    (r"APM:NPM$",       r"n-3e\(3\)",           r("-εῖς")),

    ## third declension (3e(5-6))

    (r"AP([FM]):NP\1$", r"n-3e\(5b\)",          r("-εις")),

    ## third declension (3f)

    (r"AP[FM]$",        r"n-3f\(1a\)",          r("-{V:}νας")),
    (r"APM$",           r"n-3f\(1b\)",          r("-{EO}νας")),
    (r"APM$",           r"n-3f\(1c\)",          r("-(ύ)?νας")),

    (r"AP[FM]$",        r"n-3f\(2a\)",          r("-{V:}ρας")),
    (r"APM$",           r"n-3f\(2b\)",          r("-{EO}ρας")),
    (r"AP[FM]$",        r"n-3f\(2c\)",          r("-(έ)?ρας")),


    ### dative singular

    ## first declension

    (r"DSF$",           r"n-1a",                r("-{EIR_ᾳ}")),
    (r"DSF$",           r"n-1a",                r("-{notEIR_ᾳ}")),
    (r"DSF$",           r"n-1b",                r("-(ῃ|ῇ)")),
    (r"DSF$",           r"n-1c",                r("-(ῃ|ῇ)")),
    (r"DSM$",           r"n-1d",                r("-{EIR_ᾳ}")),
    (r"DSM$",           r"n-1e",                r("-(ᾳ|ᾷ)")),
    (r"DSM$",           r"n-1f",                r("-(ῃ|ῇ)")),
    (r"DSF$",           r"n-1h",                r("-(ῃ|ῇ)")),

    ## second declension

    (r"DS.$",           r"n-2.",                r("-(ῳ|ῷ)")),

    ## third declension (3a & 3b & 3c(1,2,3))

    (r"DSM$",           r"n-3a\(1\)",           r("-πι")),
    (r"DS[FM]$",        r"n-3b\(1\)",           r("-(κι|κί)")),
    (r"DSF$",           r"n-3b\(2\)",           r("-(γι|γί)")),
    (r"DSF$",           r"n-3c\(1\)",           r("-(τι|τί)")),
    (r"DSF$",           r"n-3c\(2\)",           r("-δι")),

    ## third declension (3c(4,5))

    (r"DSN$",           r"n-3c\(4\)",           r("-ματι")),
    (r"DSM$",           r"n-3c\(5b\)",          r("-ντι")),

    ## third declension (3c(6))

    (r"DSN$",           r"n-3c\(6a\)",          r("-ατι")),
    (r"DSN$",           r"n-3c\(6[bc]\)",       r("-(τι|τί)")),

    ## third declension (3d)

    (r"DSN$",           r"n-3d\((1|2.)\)",      r("-ει")),

    ## third declension (3e(1-4))

    (r"DS[FM]$",        r"n-3e\(1\)",           r("-(υ|ύ)ϊ")),
    (r"DSM$",           r"n-3e\(3\)",           r("-εῖ")),
    (r"DSM$",           r"n-3e\(4\)",           r("-οΐ")),

    ## third declension (3e(5-6))

    (r"DSF$",           r"n-3e\(5b\)",          r("-ει")),

    ## third declension (3f)

    (r"DS.$",           r"n-3f\(1a\)",          r("-{V:}ν(ι|ί)")),
    (r"DS[FM]$",        r"n-3f\(1b\)",          r("-{EO}νι")),

    (r"DS.$",           r"n-3f\(2a\)",          r("-{V:}ρ(ι|ί)")),
    (r"DSM$",           r"n-3f\(2b\)",          r("-{EO}ρι")),
    (r"DS[FM]$",        r"n-3f\(2c\)",          r("-{C}ρί")),


    ### dative plural

    ## first declension

    (r"DP.$",           r"n-1.",                r("-(αις|αῖς)")),

    ## second declension

    (r"DP.$",           r"n-2.",                r("-(οις|οῖς)")),

    ## third declension (3a & 3b & 3c(1,2,3))

    (r"DPF$",           r"n-3b\([1-3]\)",       r("-(ξι\(ν\)|ξί\(ν\))")),
    (r"DP[FM]$",        r"n-3c\([12]\)",        r("-(σι\(ν\)|σί\(ν\))")),

    ## third declension (3c(4,5,6))

    (r"DP[MN]$",        r"n-3c\((4|5.|6.)\)",   r("-(σι\(ν\)|σί\(ν\))")),

    ## third declension (3d)

    (r"DPN$",           r"n-3d\(2b\)",          r("-σι\(ν\)")),

    ## third declension (3e(1-4))

    (r"DPM$",           r"n-3e\(3\)",           r("-εῦσι\(ν\)")),

    ## third declension (3e(5-6))

    (r"DP[FM]$",        r"n-3e\(5b\)",          r("-εσι\(ν\)")),

    ## third declension (3f)

    (r"DPM$",           r"n-3f\(1a\)",          r("-{V:}σι\(ν\)")),
    (r"DP[FM]$",        r"n-3f\(1b\)",          r("-{EO}σ(ι|ί)\(ν\)")),
    (r"DPM$",           r"n-3f\(1c\)",          r("-σί\(ν\)")),

    (r"DPM$",           r"n-3f\(2a\)",          r("-{V:}σι\(ν\)")),
    (r"DPM$",           r"n-3f\(2c\)",          r("-{C}ράσι\(ν\)")),


    ## genitive singular

    ## first declension

    (r"GSF$",           r"n-1[bch]",            r("-(ης|ῆς)")),
    (r"GSM$",           r"n-1[df]",             r("-(ου|οῦ)")),           # 110
    (r"GSM$",           r"n-1e",                r("-(α|ᾶ)")),

    ## second declension

    (r"GS.$",           r"n-2[a-d]",            r("-(ου|οῦ)")),           # 112

    ## third declension (3a & 3b & 3c(1,2,3))

    (r"GSF$",           r"n-3a\(1\)",           r("-(πος|πός)")),
    (r"GS[FM]$",        r"n-3b\(1\)",           r("-(κος|κός)")),
    (r"GS[FM]$",        r"n-3b\(2\)",           r("-(γος|γός)")),
    (r"GS[FM]$",        r"n-3c\(1\)",           r("-(τος|τός)")),
    (r"GS[FM]$",        r"n-3c\(2\)",           r("-(δος|δός)")),

    ## third declension (3c(4,5))

    (r"GSN$",           r"n-3c\(4\)",           r("-ματος")),
    (r"GSM$",           r"n-3c\(5.\)",          r("-ντος")),

    ## third declension (3c(6))

    (r"GSN$",           r"n-3c\(6.\)",          r("-(τος|τός)")),

    ## third declension (3d)

    (r"GS[FN]$",        r"n-3d\((2b|3)\)",      r("-(ους|οῦς)")),

    ## third declension (3e(1-4))

    (r"GS[FM]$",        r"n-3e\(1\)",           r("-ύος")),
    (r"GSM$",           r"n-3e\(3\)",           r("-έως")),
    (r"GSM$",           r"n-3e\(4\)",           r("-οός$")),

    ## third declension (3e(5-6))

    (r"GS.$",           r"n-3e\(5.\)",          r("-εως")),

    ## third declension (3f)

    (r"GS.$",           r"n-3f\(1a\)",          r("-{V:}νος")),           # 126
    (r"GS[FM]$",        r"n-3f\(1b\)",          r("-{EO}νος")),

    (r"GS.$",           r"n-3f\(2a\)",          r("-{V:}ρ(ο|ό)ς")),
    (r"GSM$",           r"n-3f\(2b\)",          r("-{EO}ρος")),
    (r"GS[FM]$",        r"n-3f\(2c\)",          r("-{C}ρός")),


    ### genitive plural

    (r"GP.$",           r"(.*)",                r("-(ων|ῶν)")),


    ### nominative singular

    ## first declension

    (r"NSF$",           r"n-1a",                r("-{EIR_α}")),           # 132
    (r"NSF$",           r"n-1a",                r("-{notEIR_α}")),

    (r"NSF$",           r"n-1b",                r("-(η|ή)")),
    (r"NSF$",           r"n-1c",                r("-α")),
    (r"NSM$",           r"n-1e",                r("-(α|ᾶ)ς")),
    (r"NSM$",           r"n-1f",                r("-(η|ή|ῆ)ς")),
    (r"NSF$",           r"n-1h",                r("-ῆ")),
    (r"NSF$",           r"n-1h",                r("-ᾶ")),

    ## second declension

    (r"NS[FM]$",        r"n-2[ab]",             r("-(ος|ός)")),

    ## third declension (3a & 3b & 3c(1,2,3))

    (r"NS[FM]$",        r"n-3a\(1\)",           r("-ψ")),
    (r"NS[FM]$",        r"n-3b\([1-3]\)",       r("-ξ")),

    (r"NS[FM]$",        r"n-3c\([12]\)",        r("-(ς|ξ)")),             # 143

    ## third declension (3c(4,5))

    (r"NSM$",           r"n-3c\(5a\)",          r("-ης")),
    (r"NSM$",           r"n-3c\(5b\)",          r("-(ων|ῶν)")),

    ## third declension (3d)

    (r"NSM$",           r"n-3d\(2a\)",          r("-ης")),

    ## third declension (3e(1-4))

    (r"NSF$",           r"n-3e\(1\)",           r("-(ὗς|ύς)")),
    (r"NSM$",           r"n-3e\(3\)",           r("-εύς")),
    (r"NSM$",           r"n-3e\(4\)",           r("-οῦς")),

    ## third declension (3e(5-6))

    (r"NS[FM]$",        r"n-3e\(5b\)",          r("-ις")),

    ## third declension (3f)

    (r"NS[FM]$",        r"n-3f\(1.\)",          r("-{V:}ν")),
    (r"NS[FM]$",        r"n-3f\(2.\)",          r("-{V:}ρ")),            # 152

    (r"NSM$",           r"n-3f\(2a\)",          r("-υς")),  # μάρτυς


    ### nominative plural

    ## first declension

    (r"NP[FM]$",        r"n-1.",                r("-(αι|αί)")),

    ## second declension

    (r"NP[FM]$",        r"n-2[ab]",             r("-(οι|οί)")),

    ## third declension (3a & 3b & 3c(1,2,3))

    (r"NPM$",           r"n-3a\(2\)",           r("-βες")),
    (r"NP[FM]$",        r"n-3b\(1\)",           r("-κες")),
    (r"NPF$",           r"n-3b\(2\)",           r("-γες")),
    (r"NPF$",           r"n-3b\(3\)",           r("-χες")),
    (r"NP[FM]$",        r"n-3c\(1\)",           r("-τες")),
    (r"NP[FM]$",        r"n-3c\(2\)",           r("-δες")),

    ## third declension (3c(4,5))

    (r"NPM$",           r"n-3c\(5.\)",          r("-ντες")),

    ## third declension (3e(1-4))

    (r"NP[FM]$",        r"n-3e\(1\)",           r("-ύες")),

    ## third declension (3f)

    (r"NPM$",           r"n-3f\(1a\)",          r("-{V:}νες")),
    (r"NPM$",           r"n-3f\(1b\)",          r("-{EO}νες")),
    (r"NPM$",           r"n-3f\(1c\)",          r("-(ύ)νες")),

    (r"NP[FM]$",        r"n-3f\(2a\)",          r("-{V:}ρες")),
    (r"NPM$",           r"n-3f\(2b\)",          r("-{EO}ρες")),
    (r"NP[FM]$",        r"n-3f\(2c\)",          r("-(έ)?ρες")),
]


if len(sys.argv) > 1:
    rule = sys.argv[1]
else:
    rule = None
rule_token_count = 0
rule_type_count = 0

fail_count = 0
with open("noun_forms_1.txt") as f:
    for line in f:
        form, mounce, parses, count = line.strip().split("|")

        match = set()
        for i, res in enumerate(REGEXES):
            parses_re, mounce_re, form_re = res
            if re.match(parses_re, parses) and \
                    re.match(mounce_re, mounce) and re.match(form_re, form):
                match.add(i)
                if rule and int(rule) == i:
                    print(form, mounce, parses, mounce_re, parses_re, count)
                    rule_token_count += int(count)
                    rule_type_count += 1

        if rule:
            continue

        if not match:
            fail_count += 1

            # print("(r\"{}$\", r\"{}\", r\"(.*){}$\"),".format(
            #     parses, mounce, form))

        stripped = strip_accents(form)
        if stripped.endswith("(ν)"):
            options = [stripped[:-3], stripped[:-3] + "ν"]
        else:
            options = [stripped]

        for option in options:
            ending_tree = []
            for j in range(1, min(6, len(option) + 1)):
                ending_tree.append(option[-j:])
            print(
                "/".join(ending_tree), match, parses, count
            )
#
#
# print("{} fails".format(fail_count))

if rule:
    print(rule_token_count, rule_type_count)
