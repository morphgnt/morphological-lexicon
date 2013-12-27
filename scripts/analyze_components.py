#!/usr/bin/env python
# coding: utf-8

import re

from morphgnt.utils import load_yaml, sorted_items


danker = load_yaml("../data-cleanup/danker-concise-lexicon/components.yaml")

for lexeme, metadata in sorted_items(danker):
    components = metadata["components"]

    if re.match(ur"Heb\.$", components):
        pass
    elif re.match(ur"Heb\. ‘[^’]+’$", components):
        pass
    elif re.match(ur"ἀ- priv\., [\u0370-\u03FF\u1F00-\u1FFF]+; ‘[^’]+’$", components):
        pass
    else:
        print lexeme
        print components
        break
