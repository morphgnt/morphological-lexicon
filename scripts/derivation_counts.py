#!/usr/bin/env python3
# coding: utf-8

from morphgnt.utils import load_yaml, sorted_items

derivation = load_yaml("derivation.yaml")
lexemes = load_yaml("lexemes.yaml")

total_count = 0
lexeme_count = 0
empty_count = 0
not_derivation = 0
multi_derivation = 0
nav_count = 0
non_nav_count = 0
other_not_in_lexemes = 0

for lexeme, metadata in sorted_items(lexemes):
    total_count += 1
    if lexeme in derivation.keys():
        lexeme_count += 1
        if derivation[lexeme]:
            if "derivation" in derivation[lexeme]:
                if len(derivation[lexeme]["derivation"]) == 1:
                    other = derivation[lexeme]["derivation"][0]
                    if other in lexemes:
                        pos1 = lexemes[lexeme]["pos"]
                        pos2 = lexemes[other]["pos"]
                        if pos1 in "NAV" and pos2 in "NAV" and pos1 != pos2:
                            nav_count += 1
                        else:
                            non_nav_count += 1
                    else:
                        other_not_in_lexemes += 1
                else:
                    multi_derivation += 1
            else:
                not_derivation += 1
        else:
            empty_count += 1


print("total in lexemes.yaml      : {}".format(total_count))
print("  total in derivation.yaml : {}".format(lexeme_count))
print("    no metadata            : {}".format(empty_count))
print("    not derivation         : {}".format(not_derivation))
print("    other not in lexemes   : {}".format(other_not_in_lexemes))
print("    nav derivation         : {}".format(nav_count))
print("    non-nav derivation     : {}".format(non_nav_count))
print("    multi derivation       : {}".format(multi_derivation))

