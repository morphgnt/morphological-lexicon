#!/usr/bin/env python
# coding: utf-8

from collections import defaultdict
import re
import sys
import unicodedata

from morphgnt.utils import load_yaml, sorted_items

lexemes = load_yaml("lexemes.yaml")


def strip_accents(s):
    return "".join((c for c in unicodedata.normalize("NFD", unicode(s)) if unicodedata.category(c) != "Mn"))


METADATA_NAMES = [
    "bdag-headword",
    "danker-entry",
    "dodson-entry",
    "mounce-headword",
]

fully_match = 0
no_tag = 0

for lexeme, metadata in sorted_items(lexemes):

    def r(metadata_name):
        v = metadata.get(metadata_name, "<missing>")
        if v:
            v = v.split(",")[0]
        return v if v != lexeme else None

    differences = defaultdict(list)
    for metadata_name in METADATA_NAMES:
        if r(metadata_name):
            differences[r(metadata_name)].append(metadata_name)

    if differences:
        print "{}:".format(lexeme.encode("utf-8"))
        for value, metadata_names in differences.items():
            tags = []
            if value.lower() == lexeme.lower():
                tags.append("case")
            elif strip_accents(value) == strip_accents(lexeme):
                tags.append("accentuation")
            elif strip_accents(value.lower()) == strip_accents(lexeme.lower()):
                tags.append("case")
                tags.append("accentuation")
            elif value.replace(u"οε", u"ου") == lexeme:
                tags.append("οε contraction")
            elif re.sub(u"ω$", u"ομαι", value) == lexeme:
                tags.append("ω/ομαι")
            elif re.sub(u"ομαι$", u"ω", value) == lexeme:
                tags.append("ω/ομαι")
            elif re.sub(u"ημι$", u"εμαι", value) == lexeme:
                tags.append("ημι/εμαι")
            elif re.sub(u"εμαι$", u"ημι", value) == lexeme:
                tags.append("ημι/εμαι")
            elif re.sub(u"ημι$", u"αμαι", value) == lexeme:
                tags.append("ημι/αμαι")
            elif re.sub(u"αμαι$", u"ημι", value) == lexeme:
                tags.append("ημι/αμαι")
            elif strip_accents(value).replace(u"ος", u"οτερος") == strip_accents(lexeme):
                tags.append("-τερος")
            elif re.sub(u"ον$", u"ος", value) == lexeme:
                tags.append("ον/ος")
            elif re.sub(u"ος$", u"ον", value) == lexeme:
                tags.append("ον/ος")
            elif re.sub(u"ός$", u"όν", value) == lexeme:
                tags.append("ον/ος")
            elif re.sub(u"ον$", u"α", value) == lexeme:
                tags.append("ον/α")
            elif re.sub(u"α$", u"ον", value) == lexeme:
                tags.append("ον/α")
            elif re.sub(u"α$", u"ον", strip_accents(value)) == strip_accents(lexeme):
                tags.append("ον/α")
            elif value.replace(u"ληψ", u"λημψ") == lexeme:
                tags.append("λη(μ)π")
            elif value.replace(u"λήπ", u"λήμπ") == lexeme:
                tags.append("λη(μ)π")
            elif value.replace(u"(ρ)ρ", u"ρ") == lexeme:
                tags.append("double ρ")
            elif value.replace(u"ρρ", u"ρ") == lexeme:
                tags.append("double ρ")
            elif value.replace(u"ρ", u"ρρ") == lexeme:
                tags.append("double ρ")
            elif value.replace(u"δ(δ)", u"δ") == lexeme:
                tags.append("double δ")
            elif value.replace(u"δδ", u"δ") == lexeme:
                tags.append("double δ")
            elif value.replace(u"δ", u"δδ") == lexeme:
                tags.append("double δ")
            elif value.replace(u"λ", u"λλ") == lexeme:
                tags.append("double λ")
            elif value.replace(u"νν", u"ν") == lexeme:
                tags.append("double ν")
            elif value.replace(u"εί", u"ί") == lexeme:
                tags.append("ει/ι")
            elif value.replace(u"ει", u"ι") == lexeme:
                tags.append("ει/ι")
            elif value.replace(u"(ε)ί", u"ί") == lexeme:
                tags.append("ει/ι")
            elif value.replace(u"(ε)ι", u"ι") == lexeme:
                tags.append("ει/ι")
            elif value.replace(u"(ε)ί", u"εί") == lexeme:
                tags.append("ει/ι")
            elif value.replace(u"(ε)ι", u"ει") == lexeme:
                tags.append("ει/ι")
            elif value.replace(u"(ν)", u"") == lexeme:
                tags.append("movable ν")
            elif value.replace(u"(ν)", u"ν") == lexeme:
                tags.append("movable ν")
            else:
                if value != "<missing>":
                    tags.append("@@@")
                    no_tag += 1
            print "    {}:".format(value.encode("utf-8"))
            print "        {}: [{}]".format("tags", ", ".join("\"{}\"".format(tag) for tag in tags))
            print "        {}: [{}]".format("sources", ", ".join("\"{}\"".format(source) for source in metadata_names))
    else:
        fully_match += 1

print >>sys.stderr, "{} fully-match; {} no-tag".format(fully_match, no_tag)
