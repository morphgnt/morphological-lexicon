#!/usr/bin/env python
# coding: utf-8

import re

from morphgnt.utils import load_yaml, sorted_items

regexes = [
    ur"s\. prec\.$",
    ur"orig\. uncertain$",
    ur"orig\. unclear$",
    ur"etym\. uncertain$",
    ur"etym\. unclear$",
    ur"Aram\.$",
    ur"Heb\.$",
    ur"Heb\. ‘[^’]+’$",
    ur"Heb\., of uncertain etymology$",
    ur"ἀ- priv\., [\u0370-\u03FF\u1F00-\u1FFF]+$",
    ur"ἀ- priv\., [\u0370-\u03FF\u1F00-\u1FFF]+; ‘[^’]+’$",
    ur"ἀ- priv\., [\u0370-\u03FF\u1F00-\u1FFF]+ =[\u0370-\u03FF\u1F00-\u1FFF]+ ‘[^’]+’ [^;]+; ‘[^’]+’$",
    ur"[\u0370-\u03FF\u1F00-\u1FFF]+$",
    ur"[\u0370-\u03FF\u1F00-\u1FFF]+, [\u0370-\u03FF\u1F00-\u1FFF]+$",
    ur"[\u0370-\u03FF\u1F00-\u1FFF]+; only in biblical usage$",
    ur"later form of [\u0370-\u03FF\u1F00-\u1FFF]+ in same sense$",
]

compiled_regexes = [re.compile(regex) for regex in regexes]

danker = load_yaml("../data-cleanup/danker-concise-lexicon/components.yaml")

first_fail = None
count = 0

for lexeme, metadata in sorted_items(danker):
    components = metadata["components"]

    matched = False
    for compiled_regex in compiled_regexes:
        if compiled_regex.match(components):
            matched = True
            break

    if matched:
        count += 1
    else:
        if not first_fail:
            first_fail = (lexeme, components)

print "{}/{} = {}%".format(count, len(danker), int(1000 * count / len(danker)) / 10)
if first_fail:
    print first_fail[0]
    print first_fail[1]
