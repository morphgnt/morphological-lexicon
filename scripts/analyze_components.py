#!/usr/bin/env python
# coding: utf-8

import re

from morphgnt.utils import load_yaml, sorted_items

regexes = [
    ur"orig. uncertain$",
    ur"Aram\.$",
    ur"Heb\.$",
    ur"Heb\. ‘[^’]+’",
    ur"Heb\., of uncertain etymology$",
    ur"ἀ- priv\., [\u0370-\u03FF\u1F00-\u1FFF]+; ‘[^’]+’",
]

compiled_regexes = [re.compile(regex) for regex in regexes]

danker = load_yaml("../data-cleanup/danker-concise-lexicon/components.yaml")

for lexeme, metadata in sorted_items(danker):
    components = metadata["components"]

    matched = False
    for compiled_regex in compiled_regexes:
        if compiled_regex.match(components):
            matched = True
            break

    if not matched:
        print lexeme
        print components
        break
