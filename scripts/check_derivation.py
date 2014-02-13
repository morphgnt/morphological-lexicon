#!/usr/bin/env python
# coding: utf-8

import sys

from morphgnt.utils import load_yaml, sorted_items

danker = load_yaml("../data-cleanup/danker-concise-lexicon/components.yaml")

derivation = load_yaml("derivation.yaml")

skipped = 0
existing = 0
added = 0
for lexeme, metadata in sorted_items(danker):
    components = metadata["components"].strip()

    print "{}:".format(lexeme.encode("utf-8"))
    if lexeme in derivation:
        if derivation[lexeme]:

            def q(key):
                if key in derivation[lexeme]:
                    if isinstance(derivation[lexeme][key], list):
                        print "    {}:".format(key)
                        for item in derivation[lexeme][key]:
                            print "        - {}".format(item.encode("utf-8"))
                    else:
                        print "    {}: {}".format(key, derivation[lexeme][key].encode("utf-8"))

            q("derivation")
            q("equal")
            q("see")
        existing += 1
    else:
        pass
        added += 1


print >>sys.stderr, "{} skipped; {} existing; {} added".format(skipped, existing, added)
