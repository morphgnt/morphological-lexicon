#!/usr/bin/env python
# coding: utf-8

import re

from morphgnt.utils import load_yaml, sorted_items

regexes = [
    ur"s\. prec\.$",
    ur"see next entry on the etymology$",
    ur"(orig|etym)\. (unclear|uncertain)$",
    ur"Aram\.$",
    ur"Heb\.$",
    ur"Heb\. ‘[^’]+’$",
    ur"Heb\., of uncertain etymology$",
    ur"ἀ- priv\., [\u0370-\u03FF\u1F00-\u1FFF]+$",
    ur"ἀ- priv\., [\u0370-\u03FF\u1F00-\u1FFF]+ ‘[^’]+’$",
    ur"ἀ- priv\., [\u0370-\u03FF\u1F00-\u1FFF]+; ‘[^’]+’$",
    ur"ἀ- priv\., [\u0370-\u03FF\u1F00-\u1FFF]+ =[\u0370-\u03FF\u1F00-\u1FFF]+ ‘[^’]+’ [^;]+; ‘[^’]+’$",
    ur"ἀ- copul\., [\u0370-\u03FF\u1F00-\u1FFF]+ ‘[^’]+’ =[^’]+’$",
    ur"[\u0370-\u03FF\u1F00-\u1FFF]+ \(ἀ- priv\., [\u0370-\u03FF\u1F00-\u1FFF]+\); ‘[^’]+’ i\. e\. ‘[^’]+’$",
    ur"[\u0370-\u03FF\u1F00-\u1FFF]+$",
    ur"[\u0370-\u03FF\u1F00-\u1FFF]+ fr\. [\u0370-\u03FF\u1F00-\u1FFF]+$",
    ur"fr\. [a-z ]+ [\u0370-\u03FF\u1F00-\u1FFF]+$",
    ur"[\u0370-\u03FF\u1F00-\u1FFF]+ ‘[^’]+’$",
    ur"[\u0370-\u03FF\u1F00-\u1FFF]+, [\u0370-\u03FF\u1F00-\u1FFF]+$",
    ur"[\u0370-\u03FF\u1F00-\u1FFF]+, [\u0370-\u03FF\u1F00-\u1FFF]+, cp\. [\u0370-\u03FF\u1F00-\u1FFF]+ and [\u0370-\u03FF\u1F00-\u1FFF]+ ‘[^’]+’$",
    ur"[\u0370-\u03FF\u1F00-\u1FFF]+; any ‘[^’]+’ or ‘[^’]+’$",
    ur"[\u0370-\u03FF\u1F00-\u1FFF]+; only in biblical usage$",
    ur"[\u0370-\u03FF\u1F00-\u1FFF]+; ‘[^’]+’, esp\. [a-z ]+$",
    ur"s\. [\u0370-\u03FF\u1F00-\u1FFF]+$",
    ur"later form of [\u0370-\u03FF\u1F00-\u1FFF]+ in same sense$",
    ur"Attic form of [\u0370-\u03FF\u1F00-\u1FFF]+$",
    ur"cp\. [\u0370-\u03FF\u1F00-\u1FFF]+ ‘[^’]+’$",
    ur"cp\. [\u0370-\u03FF\u1F00-\u1FFF]+; ‘[^’]+’$",
    ur"cp\. [\u0370-\u03FF\u1F00-\u1FFF]+ ‘[^’]+’, [^;]+; cp\. our ‘[^’]+’ in ref\. to [a-z ]+$",
    ur"cp\. [\u0370-\u03FF\u1F00-\u1FFF]+ ‘[^’]+’ in Persia$",
    ur"Skt\. assoc\.$",
    ur"Skt\. assoc., cp. [\u0370-\u03FF\u1F00-\u1FFF]+$",
    ur"Skt\. yájati ‘[^’]+’$",
    ur"Skt. =Lat. ager ‘piece of land’$",
    ur"Roman cognomen$",
    ur"[a-z ]+; [a-zA-Z ]+ [\u0370-\u03FF\u1F00-\u1FFF]+ ‘[^’]+’ [a-z/, ]+ ‘[^’]+’; [a-zA-Z., ]+ ‘[^’]+’$",
    ur"later form of [\u0370-\u03FF\u1F00-\u1FFF]+\. IE, cp\. [\u0370-\u03FF\u1F00-\u1FFF]+$",
    ur"etym\. complex, cp\. [A-Za-z. ]+ ‘[^’]+’$",
    ur"[\u0370-\u03FF\u1F00-\u1FFF]+ \(ἀ- priv\., [\u0370-\u03FF\u1F00-\u1FFF]+\) ‘[^’]+’, fr\. [\u0370-\u03FF\u1F00-\u1FFF]+$",
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
