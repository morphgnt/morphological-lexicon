#!/usr/bin/env python3
# coding: utf-8

from difflib import ndiff
import sys
import unicodedata

from morphgnt.utils import load_yaml, sorted_items

derivation = load_yaml("derivation.yaml")
lexemes = load_yaml("lexemes.yaml")


def strip_accents(s):
    return "".join((c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn"))


def diff(word1, word2):
    result = ""
    state = 0
    add = ""
    sub = ""
    for x in ndiff(strip_accents(lexeme), strip_accents(other)):
        if state == 0:
            if x[:2] == "  ":
                result += "."
                state = 1
            elif x[:2] == "- ":
                sub += x[2:]
                state = 2
            elif x[:2] == "+ ":
                add += x[2:]
                state = 2
            else:
                print("@@@", x)
                sys.exit(1)
        elif state == 1:
            if x[:2] == "  ":
                pass
            elif x[:2] == "- ":
                sub += x[2:]
                state = 2
            elif x[:2] == "+ ":
                add += x[2:]
                state = 2
            else:
                print("@@@", x)
                sys.exit(1)
        elif state == 2:
            if x[:2] == "  ":
                result += u"{}/{}.".format(add, sub)
                add = ""
                sub = ""
                state = 1
            elif x[:2] == "- ":
                sub += x[2:]
            elif x[:2] == "+ ":
                add += x[2:]
            else:
                print("@@@", x)
                sys.exit(1)
        else:
            print("@@@ state", state)
            sys.exit(2)
    if sub or add:
        result += u"{}/{}".format(add, sub)
    return result


for lexeme, metadata in sorted_items(lexemes):
    if lexeme in derivation.keys():
        if derivation[lexeme]:
            if "derivation" in derivation[lexeme]:
                if len(derivation[lexeme]["derivation"]) == 1:
                    other = derivation[lexeme]["derivation"][0]
                    if other in lexemes:
                        pos1 = lexemes[lexeme]["pos"]
                        pos2 = lexemes[other]["pos"]
                        morphcat1 = lexemes[lexeme].get("mounce-morphcat")
                        morphcat2 = lexemes[other].get("mounce-morphcat")
                        if pos1 in "NAV" and pos2 in "NAV" and pos1 != pos2:
                            print("{}{} {} {}_{} {} {}".format(
                                pos1,
                                pos2,
                                diff(lexeme, other),
                                morphcat1,
                                morphcat2,
                                lexeme,
                                other,
                            ))
