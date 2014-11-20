#!/usr/bin/env python3
# coding: utf-8

from morphgnt.utils import load_yaml, sorted_items

derivation = load_yaml("derivation.yaml")
lexemes = load_yaml("lexemes.yaml")

for lexeme, metadata in sorted_items(lexemes):
    if lexeme in derivation.keys():
        if derivation[lexeme]:
            if "derivation" in derivation[lexeme]:
                if len(derivation[lexeme]["derivation"]) > 1:
                    pos1 = lexemes[lexeme]["pos"]
                    morphcat1 = lexemes[lexeme].get("mounce-morphcat")

                    others = derivation[lexeme]["derivation"]
                    pos2s = []
                    morphcat2s = []

                    for other in others:
                        if other in lexemes:
                            pos2s.append(lexemes[other]["pos"])
                            morphcat2s.append(lexemes[other].get("mounce-morphcat", "?"))
                        else:
                            pos2s.append("?")
                            morphcat2s.append("?")

                    print("{} {} {} {} {} {}".format(
                        pos1,
                        "+".join(pos2s),
                        morphcat1,
                        "+".join(str(x) for x in morphcat2s),
                        lexeme,
                        "+".join(others),
                    ))

            else:
                pass
        else:
            pass
