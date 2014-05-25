#!/usr/bin/env python3

from morphgnt.utils import load_yaml, load_wordset, sorted_items

lexemes = load_yaml("lexemes.yaml")
already = load_wordset("nominal-indeclinable.txt")

for lexeme, metadata in sorted_items(lexemes):
    danker = metadata.get("danker-entry", "")
    dodson_pos = metadata.get("dodson-pos", "")
    mounce_morphcat = metadata.get("mounce-morphcat", "")

    if (
        lexeme in already or
        dodson_pos == "N-PRI" or
        mounce_morphcat == "n-3g(2)"
    ):
        print("{:20}|{:45}|{:10}|{:10}|{:5}".format(
            lexeme,
            danker,
            dodson_pos,
            mounce_morphcat,
            "yes" if lexeme in already else "no",
        ))

        if lexeme in already:
            already.remove(lexeme)

print(already)
