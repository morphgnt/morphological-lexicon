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
    
    # verbs missing in morphcat
    r"V@V@None",
    
    # verbs with unknown morphcat
    r"V@V@\?\?", # @@@
    
    # verbs missing in dodson and morphcat
    r"V@None@None",
    
    # verbs with two morphcats
    r"V@V@v-[0-9a-z\(\)]+; v-[0-9a-z\(\)]+$", # @@@
    
    # compound verbs
    r"V@V@cv-[0-9a-z\(\)]+$",
    
    # compound verbs missing in dodson
    r"V@None@cv-[0-9a-z\(\)]+$",
    
    # compound verbs missing full morphcat
    r"V@V@cv-$", # @@@
    
    # compound verbs that dodson thinks can be adjectives
    r"V@A,V@cv-[0-9a-z\(\)]+$", # @@@
    
    # verbs that morphcat thinks is an adjective
    r"V@V@a-1a\(1\)$", # @@@
    
    # ἰδού/ἴδε
    r"X/V@V@\?\?$", # @@@
    r"X/V@INJ@None$", # @@@
    
    # adjectives
    r"A@A@a-[0-9a-z\(\)]+$",
    
    # adjective missing in dodson
    r"A@None@a-[0-9a-z\(\)]+$",
    
    # adjective missing in morphcat
    r"A@A@None$",
    
    # adjective missing in dodson and morphcat
    r"A@None@None$",
    
    # adjectives that dodson has as adverbs
    r"A@A,ADV@a-[0-9a-z\(\)]+$", # @@@
    r"A@A,ADV-C@a-1a\(2a\)$", # @@@
    r"A@ADV-S@a-1a\(1\)$", # @@@
    
    # adjectives that tisch has as adverbs
    r"A/ADV-S\?@A@a-1a\(2a\)$", # @@@
    r"A/ADV-C\?@None@None$", # @@@
    r"A/ADV-C@A@a-1a\(1\)$", # @@@
    
    # adjectives that are numbers
    r"A@A,A-NUI@a-5$", # @@@
    r"A@A-NUI@n-3g\(2\)$", # @@@
    r"A@A@n-3g\(2\)$", # @@@
    
    # adjective / adverb conflation
    r"A/ADV@ADV@\['a-1a\(1\)', 'adverb'\]$", # @@@
    
    # nouns
    r"N@N:M@n-1a$", # @@@
    r"N@N:F@n-1a$", # @@@
    r"N@N:F@n-1b$",
    r"N@N:F@n-1c$",
    r"N@N:M@n-1d$",
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
    
    # indeclinable hebrew nouns
    r"N/HEB@HEB@n-3g\(2\)$",
    
    # nouns with multiple genders (according to dodson)
    r"N@N:F,N:N@n-1a$", # @@@
    r"N@N:M,N:N@n-2a$", # @@@
    r"N@N:F,N:M@n-2a$", # @@@
    r"N@N:F,N:N@n-2c$", # @@@
    r"N@N:M,N:N@n-3[0-9a-z\(\)]+$", # @@@
    r"N@N:M,N:N@\['n-2c', 'n-2a'\]$", # @@@
    
    r"\['N', 'X'\]@\['N:M', 'PRT'\]@None", # @@@
    
    # nouns missing in dodson
    r"N@None@n-[0-9a-z\(\)]+$", # @@@
    
    # nouns missing in morphcat
    r"N@N:M@None$",
    r"N@N:F@None$",
    
    # nouns missing in dodson and morphcat
    r"N@None@None$",
    
    # noun / adjective / cross-over conflation
    r"A@N:M@n-1f$", # @@@
    r"N@A@a-2a$", # @@@
    r"N/A@A@n-2a$", # @@@
    r"A@A@n-2a$", # @@@
    r"A@A@n-2b$", # @@@
    r"A/N@N:F@n-3c\(2\)$", # @@@
    r"A/N@N:N@n-2c$", # @@@
    r"A/N@N:M@a-3a$", # @@@
    r"A@A,N:F,N:M@a-1a\(2a\)$", # @@@
    r"N@A,N:M@\['n-2a', 'a-1a\(2a\)'\]$", # @@@
    r"A/N@N:F@n-1a$", # @@@
    r"N/A@A@a-3a$", # @@@
    
    r"N/ADV-K@ADV-K@adverb$", # @@@
    
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
    r"RI/A@A@a-1a\(2a\)$", # @@@
    r"RI@I@a-1a\(1\)$", # @@@
    
    # correlative pronoun
    r"RR/K@K@a-1a\(2a\)$", # @@@
    r"RR/K@K,R@a-1a\(1\)$", # @@@
    
    # correlative OR interrogative pronoun
    r"RI/Q@Q@a-1a\(2a\)$", # @@@
    
    # personal pronouns
    r"RP@P@a-1a\(2b\)$", # @@@
    r"RP1@P@a-5$", # @@@
    r"RP2@P@a-5$", # @@@
    r"RP1/P-K@P@a-5$", # @@@
    
    # relative pronouns
    r"RR@R@a-1a\(2b\)$",
    
    # possessive pronouns
    r"A/RP1@S@a-1a\(2a\)$", # @@@
    r"A/S1@S@a-1a\(1\)$", # @@@
    r"A/S-2S@S@a-1a\(2a\)$", # @@@
    r"A/S-2P@S@a-1a\(1\)$", # @@@
    
    # indefinite pronoun
    r"RI/X@X@a-4b\(2\)$", # @@@
    r"RI/A@A@a-1a\(1\)$", # @@@
    
    r"C@CONJ@conj$",
    r"D@ADV@adverb$",
    r"P@PREP@prep$",
    r"X@PRT@particle$",
    
    r"C@CONJ@particle$", # @@@
    r"C/ADV@ADV@adverb$", # @@@
    r"C/ADV@ADV@particle$", # @@@
    r"C/ADV@ADV,ADV-I@particle$", # @@@
    r"C/D@ADV@conj$", # @@@
    r"C/ADV@ADV@conj$", # @@@
    r"C/PRT@PRT@particle$", # @@@
    r"C/PRT-I@PRT-I@particle$", # @@@
    r"C/COND@COND@particle$", # @@@
    r"C/COND-K@COND-K@particle$", # @@@
    r"C/CONJ-N@CONJ-N@adverb$", # @@@
    r"C/CONJ-N@CONJ-N@conj$", # @@@
    r"C/D@ADV@adverb$", # @@@
    r"C/ADV@ADV@adverb; co$", # @@@
    
    # adverbs missing in dodson
    r"D@None@adverb$",
    
    # adverbs missing in morphcat
    r"D@ADV@None$", 
    
    r"D/ADV-S@ADV-S@adverb$", # @@@
    r"D@ADV-S@adverb$", # @@@
    r"D@ADV-S@None$", # @@@
    r"D/ADV-N@ADV-N@adverb$", # @@@
    r"D@ADV-N@adverb$", # @@@
    r"D@ADV-I@adverb$", # @@@
    r"D@ADV,ADV-C@adverb$", # @@@
    
    r"D@None@particle$", # @@@
    r"D/CONJ-N@CONJ-N@particle$", # @@@
    r"D/CONJ@CONJ@adverb$", # @@@
    r"D/PRT-N@PRT-N@particle$", # @@@
    r"D/PRT-N@PRT-N@adverb$", # @@@
    
    r"P/ADV@ADV@adverb$", # @@@
    r"P/ADV@ADV@prep$", # @@@
    r"P/ADV@ADV@adverb; pr$", # @@@
    r"P/D@ADV@adverb$", # @@@
    r"P@ADV,PREP@adverb$", # @@@
    r"P/ADV@ADV@\?\?$", # @@@
    r"P/ADV@None@None$", # @@@
    
    r"X/HEB@HEB@particle$", # @@@
    r"X/COND@COND@conj$", # @@@
    r"X/INJ@INJ,N-OI@interjectio$", # @@@
    r"X/INJ@INJ@interj$", # @@@
    r"X/ADV-N@ADV-N@particle$", # @@@
    r"X/PRT-I@PRT-I,PRT-N@adverb$", # @@@
    r"X@PRT-I@particle$", # @@@
    r"X@PRT-N@adverb$", # @@@
    r"X/V@V@particle$", # @@@
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
