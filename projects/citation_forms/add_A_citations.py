#!/usr/bin/env python3

import sys

from morphgnt.utils import load_yaml, sorted_items

lexemes = load_yaml("lexemes.yaml")

missed = []
# used = []

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
        if metadata["pos"] in ["A", "N/A", "A/N"]:
            if metadata.get("danker-entry"):
                print(
                    "    full-citation-form: {}".format(
                        metadata["danker-entry"]
                    )
                )

    q("bdag-headword")
    q("danker-entry")
    q("dodson-entry")
    q("mounce-headword")
    q("strongs")
    q("gk")
    q("dodson-pos")
    q("gloss")
    q("mounce-morphcat")


# print("N missed", file=sys.stderr)
# for word in n_missed:
#     print("\t{}".format(word), file=sys.stderr)
#
# print("non-N found", file=sys.stderr)
# for word in non_n_found:
#     print("\t{}".format(word), file=sys.stderr)
#
# print("not used", file=sys.stderr)
# for word in not_used:
#     print("\t{}".format(word), file=sys.stderr)
#
print(
    "{}".format(
        len(missed),
    ),
    file=sys.stderr,
)
