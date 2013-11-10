#!/usr/bin/env python
# coding: utf-8

import re

from pyuca import Collator
collator = Collator()

from morphgnt.utils import load_yaml


lexemes = load_yaml("lexemes.yaml")

regexes = [
    # verbs
    r"V@V@v-[0-9a-z\(\)]+$",
    
    # verbs missing in dodson
    r"V@None@v-[0-9a-z\(\)]+$",
    
    # compund verbs
    r"V@V@cv-[0-9a-z\(\)]+$",
    
    # compound verbs missing full morphcat
    r"V@V@cv-$", # @@@
    
    # ἰδού
    r"X/V@V@\?\?$", # @@@
    
    r"A@A@a-[0-9a-z\(\)]+$",
    
    # adjective missing in dodson
    r"A@None@a-[0-9a-z\(\)]+$",
    
    # adjectives that dodson has as adverbs
    r"A@A,ADV@a-1a\(1\)$", # @@@
    r"A@A,ADV-C@a-1a\(2a\)$", # @@@
    r"A@ADV-S@a-1a\(1\)$", # @@@
    
    # nouns
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
    
    # 3rd declension nouns
    r"N@N:M@n-3[0-9a-z\(\)]+$",
    r"N@N:F@n-3[0-9a-z\(\)]+$",
    r"N@N:N@n-3[0-9a-z\(\)]+$",
    
    # indeclinable proper nouns
    r"N@N-PRI@n-3g\(2\)$",
    
    # nouns with multiple genders (according to dodson)
    r"N@N:M,N:N@n-2a$", # @@@
    r"N@N:F,N:M@n-2a$", # @@@
    r"N@N:F,N:N@n-2c$", # @@@
    r"N@N:M,N:N@n-3[0-9a-z\(\)]+$", # @@@
    
    # nouns missing in dodson
    r"N@None@n-[0-9a-z\(\)]+$", # @@@
    
    # noun / adjective / cross-over conflation
    r"A@N:M@n-1f$", # @@@
    r"N@A@a-2a$", # @@@
    r"N/A@A@n-2a$", # @@@
    r"A@A@n-2a$", # @@@
    r"A@A,N:F,N:M@a-1a\(2a\)$", # @@@
    r"N@A,N:M@\['n-2a', 'a-1a\(2a\)'\]$", # @@@
    
    # article
    r"RA@T@a-1a\(2b\)$",
    
    # demonstratives
    r"RD@D@a-1a\(2b\)$",
    
    # reciprocal pronoun
    r"RP/C@C@a-1a\(2b\)$", # @@@
    
    # reflexive pronouns
    r"RP/F-2@F@a-1a\(2b\)$", # @@@
    r"RP1/F@F@a-1a\(2a\)$", # @@@
    r"RP2/F@F@a-1a\(2b\)$", # @@@
    
    # interrogative pronoun
    r"RI/X@I@a-4b\(2\)$", # @@@
    
    # correlative pronoun
    r"RR/K@K@a-1a\(2a\)$", # @@@
    
    # correlative OR interrogative pronoun
    r"RI/Q@Q@a-1a\(2a\)$", # @@@
    
    # personal pronouns
    r"RP@P@a-1a\(2b\)$", # @@@
    r"RP1@P@a-5$", # @@@
    r"RP2@P@a-5$", # @@@
    
    # relative pronouns
    r"RR@R@a-1a\(2b\)$",
    r"RR/R@R@a-1a\(2b\)$", # @@@
    
    # possessive pronouns
    r"A/RP1@S@a-1a\(2a\)$", # @@@
    r"A/S1@S@a-1a\(1\)$", # @@@
    r"A/S-2S@S@a-1a\(2a\)$", # @@@
    
    # indefinite pronoun
    r"RI/X@X@a-4b\(2\)$", # @@@
    
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
fails = []

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
        fails.append("{}: {}@{}@{}".format(lexeme.encode("utf-8"), pos, dodson_pos, morphcat))

for fail in fails:
    print fail
print "{}/{} = {}%".format(match, total, int(1000 * match / total) / 10)
