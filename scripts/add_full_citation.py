#!/usr/bin/env python3

import sys

from morphgnt.utils import load_yaml, sorted_items

lexemes = load_yaml("lexemes.yaml")
full_citation = load_yaml("../greek-vocab-assessment/headwords.txt")

n_missed = []
non_n_found = []
used = []

for lexeme, metadata in sorted_items(lexemes):
    print("{}:".format(lexeme))

    def q(metadata_name):
        if metadata_name in metadata:
            print(
                "    {}: {}".format(
                    metadata_name,
                    metadata[metadata_name]
                )
            )

    q("pos")

    if "full-citation-form" in metadata:
        print(
            "    full-citation-form: {}".format(
                metadata["full-citation-form"]
            )
        )
    else:
        if lexeme in full_citation:
            print(
                "    full-citation-form: {}".format(full_citation[lexeme])
            )
            used.append(lexeme)
            if metadata["pos"] != "N":
                non_n_found.append(lexeme)
        else:
            if metadata["pos"] == "N":
                n_missed.append(lexeme)

    q("bdag-headword")
    q("danker-entry")
    q("dodson-entry")
    q("mounce-headword")
    q("strongs")
    q("gk")
    q("dodson-pos")
    q("gloss")
    q("mounce-morphcat")

not_used = []
for lexeme in full_citation:
    if lexeme not in used:
        not_used.append(lexeme)

print("N missed", file=sys.stderr)
for word in n_missed:
    print("\t{}".format(word), file=sys.stderr)

print("non-N found", file=sys.stderr)
for word in non_n_found:
    print("\t{}".format(word), file=sys.stderr)

print("not used", file=sys.stderr)
for word in not_used:
    print("\t{}".format(word), file=sys.stderr)

print(
    "{} {} {}".format(
        len(n_missed),
        len(non_n_found),
        len(not_used)
    ),
    file=sys.stderr,
)
