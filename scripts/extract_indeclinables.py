#!/usr/bin/env python3

from morphgnt.utils import load_yaml

lexemes = load_yaml("lexemes.yaml")

for lexeme in lexemes:
    if lexemes[lexeme].get("mounce-morphcat") == "n-3g(2)":
        print(lexeme)
