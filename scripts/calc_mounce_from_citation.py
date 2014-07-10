#!/usr/bin/env python3

import re
import unicodedata

from morphgnt.utils import load_yaml

from noun_citation_form_data import NOUN_CITATION_FORMS

lexemes = load_yaml("lexemes.yaml")

ACUTE = u"\u0301"
GRAVE = u"\u0300"
CIRCUMFLEX = u"\u0342"


def strip_accents(w):
    return "".join(
        unicodedata.normalize("NFC", "".join(
            component
            for component in unicodedata.normalize("NFD", ch)
            if component not in [ACUTE, GRAVE, CIRCUMFLEX]
        )) for ch in w
    )


def r(s):
    s = re.sub("{art}", "(ὁ|ἡ|το)", s)
    s = re.sub("{V}", "([αεηιουωϊἀὑὠ]|αι|ει)", s)
    return s


for lexeme in [
    "ψίξ",
]:

    metadata = lexemes[lexeme]

    pos = metadata.get("pos")
    full_citation = metadata.get("full-citation-form")
    dodson_pos = metadata.get("dodson-pos", "")
    mounce_morphcat = metadata.get("mounce-morphcat", "")

    if re.match(r"(\w+), (\w+), (\w+)$", full_citation):
        if isinstance(mounce_morphcat, list):
            mounce_morphcat = ";".join(mounce_morphcat)

        node = NOUN_CITATION_FORMS

        level = 1
        while node:
            success = []
            for child in node:
                match_tuple, key, children = child
                end, cat, dodson = match_tuple
                end = r(end)
                if (re.search(end, strip_accents(full_citation))):
                    success.append(((key, cat), children))
            if len(success) != 1:
                print("testing: {}".format(full_citation))
                print("found {} matches at level {}".format(len(success), level))
                print("; ".join(str(s[0]) for s in success))
                quit()
            node = success[0][1]
            level += 1

        print(lexeme, success[0][0])
    else:
        print("no matching citation form for {}".format(lexeme))
