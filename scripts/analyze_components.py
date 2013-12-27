#!/usr/bin/env python
# coding: utf-8

import re

from morphgnt.utils import load_yaml, sorted_items

regexes = [
    ur"Heb\.$",
    ur"Heb\. ‘[^’]+’",
    ur"ἀ- priv\., [\u0370-\u03FF\u1F00-\u1FFF]+; ‘[^’]+’",
]

danker = load_yaml("../data-cleanup/danker-concise-lexicon/components.yaml")

for lexeme, metadata in sorted_items(danker):
    components = metadata["components"]

    matched = False
    for regex in regexes:
        if re.match(regex, components):
            matched = True
            break

    if not matched:
        print lexeme
        print components
        break
