#!/usr/bin/env python

import re

from pyuca import Collator
collator = Collator()

from morphgnt.utils import load_yaml


lexemes = load_yaml("lexemes.yaml")

regexes = [
    r"V@V@v-[0-9a-z\(\)]+$",
    r"V@V@cv-[0-9a-z\(\)]+$",
    r"V@V@cv-$", # @@@
    
    r"V@None@v-1d\(1a\)$", # @@@
    r"X/V@V@\?\?$", # @@@
    
    r"A@A@a-[0-9a-z\(\)]+$",
    
    r"A@None@a-1a\(1\)$", # @@@
    r"A@A,ADV@a-1a\(1\)$", # @@@
    r"A@A,ADV-C@a-1a\(2a\)$", # @@@
    r"A@ADV-S@a-1a\(1\)$", # @@@
    
    r"N@N:F@n-1a$",
    r"N@N:F@n-1b$",
    r"N@N:F@n-1c$",
    r"N@N:M@n-1e$",
    r"N@N:M@n-1f$",
    r"N@N:F@n-1h$",
    r"N@N:M@n-2a$",
    r"N@N:F@n-2b$",
    r"N@N:N@n-2c$",
    r"N@N:M@n-2e$",
    
    r"N@None@n-1a$", # @@@
    r"A@N:M@n-1f$", # @@@
    r"N@N:M,N:N@n-2a$", # @@@
    r"N@N:F,N:M@n-2a$", # @@@
    r"N@N:F,N:N@n-2c$", # @@@
    
    r"N@N:M@n-3[0-9a-z\(\)]+$",
    r"N@N:F@n-3[0-9a-z\(\)]+$",
    r"N@N:N@n-3[0-9a-z\(\)]+$",
    
    r"N@N:M,N:N@n-3[0-9a-z\(\)]+$", # @@@
    r"N@A@a-2a$", # @@@
    r"N/A@A@n-2a$", # @@@
    r"A@A@n-2a$", # @@@
    r"A@A,N:F,N:M@a-1a\(2a\)$", # @@@
    r"N@A,N:M@\['n-2a', 'a-1a\(2a\)'\]$", # @@@
    
    r"N@None@n-3g\(1\)$", # @@@
    r"N@N-PRI@n-3g\(2\)$",
    
    r"RA@T@a-1a\(2b\)$",
    r"RD@D@a-1a\(2b\)$",
    r"RI/Q@Q@a-1a\(2a\)$", # @@@
    r"RI/X@X@a-4b\(2\)$", # @@@
    r"RI/X@I@a-4b\(2\)$", # @@@
    r"RR@R@a-1a\(2b\)$",
    r"RR/R@R@a-1a\(2b\)$", # @@@
    r"RR/K@K@a-1a\(2a\)$", # @@@
    
    r"RP/C@C@a-1a\(2b\)$", # @@@
    r"RP@P@a-1a\(2b\)$", # @@@
    r"RP/F-2@F@a-1a\(2b\)$", # @@@
    r"RP1@P@a-5$", # @@@
    r"RP1/F@F@a-1a\(2a\)$", # @@@
    r"RP2/F@F@a-1a\(2b\)$", # @@@
    r"RP2@P@a-5$", # @@@
    
    r"A/RP1@S@a-1a\(2a\)$", # @@@
    r"A/S1@S@a-1a\(1\)$", # @@@
    r"A/S-2S@S@a-1a\(2a\)$", # @@@
    
    r"C@CONJ@conj$",
    r"D@ADV@adverb$",
    r"P@PREP@prep$",
    r"X@PRT@particle$",
    
    r"C@CONJ@particle$", # @@@
    r"C/ADV@ADV@adverb$", # @@@
    r"C/ADV@ADV@particle$", # @@@
    r"C/D@ADV@conj$", # @@@
    r"C/PRT@PRT@particle$", # @@@
    r"C/COND@COND@particle$", # @@@
    r"C/CONJ-N@CONJ-N@adverb$", # @@@
    r"C/D@ADV@adverb$", # @@@
    
    r"D/ADV-S@ADV-S@adverb$", # @@@
    r"D/ADV-N@ADV-N@adverb$", # @@@
    r"D/CONJ-N@CONJ-N@particle$", # @@@
    r"D/PRT-N@PRT-N@particle$", # @@@
    r"D/PRT-N@PRT-N@adverb$", # @@@
    
    r"P/ADV@ADV@adverb$", # @@@
    r"P/ADV@ADV@prep$", # @@@
    r"P/ADV@ADV@adverb; pr$", # @@@
    r"P/D@ADV@adverb$", # @@@
    
    r"X/HEB@HEB@particle$", # @@@
    r"X/COND@COND@conj$", # @@@
    r"X/INJ@INJ,N-OI@interjectio$", # @@@
]

match = 0
total = 0
first_fail = None

for lexeme, metadata in sorted(lexemes.items(), key=lambda x: collator.sort_key(x[0])):
    pos = metadata.get("pos")
    dodson_pos = metadata.get("dodson-pos")
    morphcat = metadata.get("mounce-morphcat")
    
    matched = False
    for regex in regexes:
        if re.match(regex, "{}@{}@{}".format(pos, dodson_pos, morphcat)):
            matched = True
            break
    
    total += 1
    if matched:
        match += 1
    else:
        if first_fail is None:
            first_fail = "{}: {}@{}@{}".format(lexeme.encode("utf-8"), pos, dodson_pos, morphcat)

print "{}/{} = {}%".format(match, total, int(1000 * match / total) / 10)
if first_fail:
    print first_fail

