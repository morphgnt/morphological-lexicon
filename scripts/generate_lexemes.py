#!/usr/bin/env python

from morphgnt import filesets
from morphgnt.utils import load_yaml

lexemes = load_yaml("lexemes.yaml")
fs = filesets.load("filesets.yaml")

def convert(ccat, robinson):
    pair = (ccat, robinson.split("-")[0])
    if pair == ("N-", "N"):
        return "N"
    elif pair == ("V-", "V"):
        return "V"
    elif pair == ("A-", "A"):
        return "A"
    elif pair == ("D-", "ADV"):
        return "D"
    elif pair == ("P-", "PREP"):
        return "P"
    elif pair == ("RD", "D"):
        return "RD"
    elif pair == ("RR", "R"):
        return "RR"
    elif pair == ("C-", "CONJ"):
        return "C"
    else:
        return "{} {}".format(ccat, robinson)


for row in fs["sblgnt-lexemes"].rows():
    if row["lemma"].decode("utf-8") not in lexemes:
        print "{}:".format(row["lemma"])
        print "    pos: {}".format(convert(row["ccat-pos"], row["robinson"]))
