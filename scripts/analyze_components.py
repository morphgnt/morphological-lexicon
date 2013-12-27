#!/usr/bin/env python

import re

from morphgnt.utils import load_yaml, sorted_items


danker = load_yaml("../data-cleanup/danker-concise-lexicon/components.yaml")

for lexeme, metadata in sorted_items(danker):
    components = metadata["components"]

    if re.match("^Heb.$", components):
        pass
    else:
        print lexeme
        print components
        break
