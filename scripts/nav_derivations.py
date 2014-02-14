#!/usr/bin/env python
# coding: utf-8

from morphgnt.utils import load_yaml, sorted_items

derivation = load_yaml("derivation.yaml")
lexemes = load_yaml("lexemes.yaml")

for lexeme, metadata in sorted_items(lexemes):
    if lexeme in derivation.keys():
        if derivation[lexeme]:
            if "derivation" in derivation[lexeme]:
                if len(derivation[lexeme]["derivation"]) == 1:
                    other = derivation[lexeme]["derivation"][0]
                    if other in lexemes:
                        pos1 = lexemes[lexeme]["pos"]
                        pos2 = lexemes[other]["pos"]
                        if pos1 in "NAV" and pos2 in "NAV" and pos1 != pos2:
                            print pos1 + pos2,
                            print lexeme.encode("utf-8"), other.encode("utf-8")

