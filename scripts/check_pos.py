#!/usr/bin/env python
# coding: utf-8

import re

from morphgnt.utils import load_yaml, sorted_items


lexemes = load_yaml("lexemes.yaml")

regexes = [
    # verbs
    r"V@V@v-[0-9a-z\(\)]+$",

    # verbs missing in dodson
    r"V@None@v-[0-9a-z\(\)]+$",

    # verbs missing in morphcat
    r"V@V@None$",

    # verbs with unknown morphcat
    r"V@V@\?\?$", # @@@

    # verbs missing in dodson and morphcat
    r"V@None@None$",

    # verbs with two morphcats
    r"V@V@v-[0-9a-z\(\)]+; v-[0-9a-z\(\)]+$", # @@@

    # compound verbs
    r"V@V@cv-[0-9a-z\(\)]+$",

    # compound verbs missing in dodson
    r"V@None@cv-[0-9a-z\(\)]+$",

    # compound verbs missing full morphcat
    r"V@V@cv-$", # @@@
    r"V@None@cv-$", # @@@

    # compound verbs that dodson thinks can be adjectives
    r"V@A,V@cv-[0-9a-z\(\)]+$", # @@@

    # verbs that morphcat thinks is an adjective
    r"V@V@a-1a\(1\)$", # @@@

    # indeclinable verb
    r"V/ARAM@None@None$", # @@@
    r"V/ARAM@ARAM@n-3g\(2\)$", # @@@
    r"V/ARAM@ARAM,HEB@n-3g\(2\)$", # @@@

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

    # adjectives that morphcat has as nouns
    r"A@A@n-3f\(2a\)$", # @@@
    r"A@None@n-3g\(2\)$", # @@@

    # adjectives that dodson has as adverbs
    r"A@A,ADV@a-[0-9a-z\(\)]+$", # @@@
    r"A@A,ADV-C@a-[0-9a-z\(\)]+$", # @@@
    r"A@ADV-S@a-1a\(1\)$", # @@@
    r"A/ADV-S@ADV-S@None$", # @@@
    r"A/ADV@ADV@adverb$", # @@@

    # adjectives that tisch has as adverbs
    r"A/ADV-S\?@A@a-1a\(2a\)$", # @@@
    r"A/ADV-C\?@None@None$", # @@@
    r"A/ADV-C@None@None$", # @@@
    r"A/ADV-C@A@a-1a\(1\)$", # @@@
    r"A/ADV-C@ADV-C@adverb$", # @@@
    r"A/ADV-C\?@ADV@adverb$", # @@@
    r"A/ADV@A@a-1a\(1\)$", # @@@
    r"A/ADV@None@None$", # @@@

    # adjectives that mounce has as adverbs
    r"A@A@adverb$", # @@@

    # adjectives that are numbers
    r"A@A,A-NUI@a-5$", # @@@
    r"A@A-NUI@n-3g\(2\)$", # @@@
    r"A@A@n-3g\(2\)$", # @@@

    r"A@A@n-3c\(2\)$", # @@@

    # adjective / adverb conflation
    r"A/ADV@ADV@\['a-1a\(1\)', 'adverb'\]$", # @@@
    r"A/ADV-C@ADV-C@None$", # @@@
    r"A/ADV-C@ADV@None$", # @@@

    # nouns
    r"N@N:M@n-1a$", # @@@
    r"N@N:F@n-1a$", # @@@
    r"N@N:M@n-1b$", # @@@
    r"N@N:F@n-1b$", # @@@
    r"N@N:F@n-1c$",
    r"N@N:M@n-1d$",
    r"N@N:M@n-1e$",
    r"N@N:M@n-1f$", # @@@
    r"N@N:F@n-1f$", # @@@
    r"N@N:M@n-1g$", # @@@
    r"N@N:F@n-1h$", # @@@
    r"N@N:M@n-1h$", # @@@
    r"N@N:M@n-2a$", # @@@
    r"N@N:F@n-2a$", # @@@
    r"N@N:N@n-2a$", # @@@
    r"N@N:M@n-2b$", # @@@
    r"N@N:F@n-2b$", # @@@
    r"N@N:N@n-2c$", # @@@
    r"N@N:F@n-2c$", # @@@
    r"N@N:M@n-2d\(1\)$",
    r"N@N:M@n-2e$", # @@@
    r"N@N:F@n-2e$", # @@@

    # 3rd declension nouns
    r"N@N:M@n-3[0-9a-z\(\)]+$",
    r"N@N:F@n-3[0-9a-z\(\)]+$",
    r"N@N:N@n-3[0-9a-z\(\)]+$",

    r"N@N-OI@n-3c\(6b\)$",
    r"N@N-OI@n-3g\(2\)$",

    # indeclinable proper nouns
    r"N@N-PRI@n-3g\(1\)$",
    r"N@N-PRI@n-3g\(2\)$",

    r"N@N-PRI@\?\?$", # @@@

    r"N@N-PRI@n-2d\(1\)$", # @@@

    r"N@N:M,N-PRI@n-3g\(1\)$", # @@@

    # indeclinable letter names
    r"N@N-LI@n-3g\(2\)$",

    # indeclinable hebrew nouns
    r"N/HEB@HEB@n-3g\(2\)$",
    r"N@HEB@n-3g\(2\)$",
    r"N/HEB@HEB,N:M@n-3g\(2\)$",

    # indeclinable aramaic nouns
    r"N/ARAM@ARAM@n-3g\(2\)$",
    r"N/ARAM@HEB@n-3g\(2\)$",
    r"N/ARAM@None@None$",

    # nouns with multiple genders (according to dodson)
    r"N@N:F,N:N@n-1a$", # @@@
    r"N@N:M,N:N@n-2a$", # @@@
    r"N@N:F,N:M@n-2a$", # @@@
    r"N@N:F,N:N@n-2c$", # @@@
    r"N@N:M,N:N@n-2c$", # @@@
    r"N@N:M,N:N@n-3[0-9a-z\(\)]+$", # @@@
    r"N@N:F,N:M@n-3[0-9a-z\(\)]+$", # @@@
    r"N@N:M,N:N@\['n-2c', 'n-2a'\]$", # @@@
    r"N@N:F,N:M@None$", # @@@
    r"N@N:F,N-PRI@n-1a$", # @@@

    r"\['N', 'X'\]@\['N:M', 'PRT'\]@None$", # @@@

    # nouns missing in dodson
    r"N@None@n-[0-9a-z\(\)]+$", # @@@

    # nouns missing in morphcat
    r"N@N:M@None$",
    r"N@N:N@None$",
    r"N@N:F@None$",
    r"N@N:M@\?\?$",

    # nouns missing in dodson and morphcat
    r"N@None@None$",
    r"N@None@\?\?$",

    # noun / adjective / cross-over conflation
    r"A@N:F@n-1a$", # @@@
    r"A@N:M@n-1f$", # @@@
    r"N@A@a-2a$", # @@@
    r"N@A@n-2a$", # @@@
    r"N@A@n-3c\(2\)$", # @@@
    r"N/A@A@n-2a$", # @@@
    r"A@A@n-2a$", # @@@
    r"A@A@n-2b$", # @@@
    r"A@A@n-3b\(2\)$", # @@@
    r"A/N@N:M@n-3c\(1\)$", # @@@
    r"A/N@N:F@n-3c\(2\)$", # @@@
    r"A/N@N:M@n-2a$", # @@@
    r"A/N@N:N@n-2c$", # @@@
    r"A/N@N:M@a-3a$", # @@@
    r"A/N@N:N@a-3a$", # @@@
    r"A/N@N:F@a-3a$", # @@@
    r"A/N@N:N@None$", # @@@
    r"A@N:N@None$", # @@@
    r"A/N@A@a-2b$", # @@@
    r"A@A,N:F,N:M@a-1a\(2a\)$", # @@@
    r"N@A,N:M@\['n-2a', 'a-1a\(2a\)'\]$", # @@@
    r"A/N@N:F@n-1a$", # @@@
    r"N/A@A@a-3a$", # @@@
    r"N/A@A@a-5$", # @@@
    r"A@A@n-3c\(6b\)$", # @@@
    r"A/N@N:M@a-1a\(1\)$", # @@@
    r"A/N@N:M@a-1a\(2a\)$", # @@@
    r"A/N@None@a-1a\(1\)$", # @@@

    r"N/ADV-K@ADV-K@adverb$", # @@@
    r"N/ADV-K@ADV-K@None$", # @@@

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
    r"C/ADV@ADV-N@adverb$", # @@@
    r"C/ADV-K@ADV-K@adverb$", # @@@
    r"C/ADV@None@adverb$", # @@@
    r"C/ADV@ADV@particle$", # @@@
    r"C/ADV@ADV,ADV-I@particle$", # @@@
    r"C/D@ADV@conj$", # @@@
    r"C/ADV@ADV@conj$", # @@@
    r"C/PRT@PRT@particle$", # @@@
    r"C/PRT-I@PRT-I@particle$", # @@@
    r"C/COND@COND@particle$", # @@@
    r"C/COND@None@particle$", # @@@
    r"C/COND-K@COND-K@particle$", # @@@
    r"C/CONJ-N@CONJ-N@adverb$", # @@@
    r"C/CONJ-N@CONJ-N@conj$", # @@@
    r"C/D@ADV@adverb$", # @@@
    r"C/ADV@ADV@adverb; co$", # @@@

    # adverbs missing in dodson
    r"D@None@adverb$",
    r"D/@@None@adverb$", # @@@

    # adverbs missing in morphcat
    r"D@ADV@None$",

    # adverbs missing in both dodson and morphcat
    r"D@None@None$",

    r"D/ADV-S@ADV-S@adverb$", # @@@
    r"D@ADV-S@adverb$", # @@@
    r"D@ADV-S@None$", # @@@
    r"D@ADV-C@adverb$", # @@@
    r"D@ADV-C@None$", # @@@
    r"D/ADV-N@ADV-N@adverb$", # @@@
    r"D@ADV-N@adverb$", # @@@
    r"D@ADV-I@adverb$", # @@@
    r"D@ADV,ADV-C@adverb$", # @@@
    r"D@ADV@prep$", # @@@
    r"D@ADV@adverb; pr$", # @@@

    r"D@None@particle$", # @@@
    r"D/CONJ-N@CONJ-N@particle$", # @@@
    r"D/CONJ@CONJ@adverb$", # @@@
    r"D/PRT-N@PRT-N@particle$", # @@@
    r"D/PRT-N@PRT-N@adverb$", # @@@
    r"D/PRT-N@None@None$", # @@@
    r"D/PRT-I@None@None$", # @@@
    r"D/PRT-I@PRT-I@adverb$", # @@@
    r"D/A\?@None@None$", # @@@
    r"D@None@conj$", # @@@
    r"D@ADV,V@adverb$", # @@@
    r"D/V@V@adverb$", # @@@

    # adverb / noun confusion
    r"D/N@None@None$", # @@@
    r"D/N@N:F@adverb$", # @@@
    r"D/ARAM@ARAM,HEB@n-3g\(2\)$", # @@@
    r"D@ADV@n-3g\(2\)$", # @@@

    # prepositions missing in dodson
    r"P@None@prep$",

    r"P/ADV@ADV@adverb$", # @@@
    r"P/ADV@ADV@prep$", # @@@
    r"P/ADV@ADV@adverb; pr$", # @@@
    r"P/D@ADV@adverb$", # @@@
    r"P@ADV,PREP@adverb$", # @@@
    r"P/ADV@ADV@\?\?$", # @@@
    r"P/ADV@None@None$", # @@@

    r"X@None@None$",
    r"X/HEB@HEB@particle$", # @@@
    r"X/COND@COND@conj$", # @@@
    r"X/INJ@INJ,N-OI@interjectio$", # @@@
    r"X/INJ@INJ@interjecti$", # @@@
    r"X/INJ@INJ@interj$", # @@@
    r"X/ADV-N@ADV-N@particle$", # @@@
    r"X/ADV@ADV@adverb$", # @@@
    r"X/ADV@None@adverb$", # @@@
    r"X/PRT-I@PRT-I,PRT-N@adverb$", # @@@
    r"X@PRT-I@particle$", # @@@
    r"X@PRT-N@adverb$", # @@@
    r"X/V@V@particle$", # @@@
    r"X/HEB@HEB@n-3g\(2\)$", # @@@
]

match = 0
total = 0
fails = []

compiled_regexes = [re.compile(regex) for regex in regexes]

for lexeme, metadata in sorted_items(lexemes):
    pos = metadata.get("pos")
    dodson_pos = metadata.get("dodson-pos")
    morphcat = metadata.get("mounce-morphcat")

    matched = False
    for compiled_regex in compiled_regexes:
        if compiled_regex.match("{}@{}@{}".format(pos, dodson_pos, morphcat)):
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
