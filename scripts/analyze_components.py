#!/usr/bin/env python
# coding: utf-8

import re

from morphgnt.utils import load_yaml, sorted_items

regex_templates = {
    "greek": ur"[\u0370-\u03FF\u1F00-\u1FFF]+",
    "gloss": ur"‘[^’]+’",
    "text": ur"[A-Za-z.,/ ]+",
    "latin": ur"[A-Za-z]+",
    "pie": ur"\*[a-z]+",
    "skt": ur"[a-zá]+",
    "ref": ur"(?:Mt) \d+:\d+",
}

regexes = [
    ur"s\. prec\.$",
    ur"s\. prec\. {greek}- entries and two next entries$",
    ur"s\. prec\. {greek}- entries; the act\., which is not used in NT ={gloss}$",
    ur"see next entry on the etymology$",
    ur"(orig|etym)\. (complex|obscure|unclear|uncertain)$",
    ur"etym\. uncertain; {gloss}$",
    ur"etym\. uncertain; {text}$",
    ur"derivation undetermined, but a root signifying {gloss} or {gloss} has claimed attention$",
    ur"Aram\.$",
    ur"Aram\. ={text}; s\. explanation {ref}$",
    ur"Heb\.$",
    ur"Heb\. {gloss}$",
    ur"Heb\., of uncertain etymology$",
    ur"ἀ- priv\., {greek}$",
    ur"ἀ- priv\., {greek} {gloss}$",
    ur"ἀ- priv\., {greek}; {gloss}$",
    ur"ἀ- priv\., {greek} ={greek} {gloss} {text}; {gloss}$",
    ur"ἀ- priv\., {greek} {gloss} fr\. {greek}$",
    ur"ἀ- priv\., {greek}, {greek}$",
    ur"ἀ- priv\., {greek}, {greek} {gloss} fr. {greek}$",
    ur"ἀ- priv\., {greek} \({greek}, {greek} {gloss}\) {gloss} or \({greek}, {greek} {gloss} fr\. {greek} {gloss}\) {gloss}$",
    ur"ἀ- priv\., {greek}, q\. v\., in sense of {gloss}; {text}$",
    ur"ἀ- copul\., {greek} {gloss}$",
    ur"ἀ- copul\., {greek} {gloss} ={gloss}$",
    ur"{greek} \(ἀ- priv\., {greek}\); {gloss} i\. e\. {gloss}$",
    ur"{greek}$",
    ur"{greek} fr\. {greek}$",
    ur"fr\. {text} {greek}$",
    ur"={greek}$",
    ur"{greek} {gloss}$",
    ur"{greek} {gloss}, {greek} {gloss}$",
    ur"{greek} {gloss}, {greek} {gloss}; {text}$",
    ur"{greek}, {greek}$",
    ur"{greek}, {greek}, cp\. {greek} and {greek} {gloss}$",
    ur"{greek} {gloss}, cp\. {greek}$",
    ur"{greek}; any {gloss} or {gloss}$",
    ur"{greek}; only in biblical usage$",
    ur"{greek}; =next entry$",
    ur"{greek} \(={greek}\); {gloss}$",
    ur"{greek}; {gloss}, esp\. {text}$",
    ur"{greek} {gloss} {text}$",
    ur"{greek}, {greek}, {greek} {gloss}$",
    ur"{greek} {gloss} {text}$",
    ur"{greek} {gloss}, {text}$",
    ur"{greek} {gloss}; in non- biblical authors freq\. in sense of {gloss}$",
    ur"{greek} {gloss}, {greek} {gloss} {text} {greek} {gloss}$",
    ur"s\. {greek}$",
    ur"later form of {greek} in same sense$",
    ur"Attic form of {greek}$",
    ur"Attic form ={greek}, etym\. uncertain$",
    ur"assoc. w. {greek}; {gloss}, also {gloss}$",
    ur"assoc. w. {greek} {text}, pl\. as in {greek} {gloss}$",
    ur"cp\. {greek}$",
    ur"cp\. {greek} {gloss}$",
    ur"cp\. {greek}; {gloss}$",
    ur"cp\. {greek} {gloss} and {greek}$",
    ur"cp\. {greek} {gloss}, {text}; cp\. our {gloss} in ref\. to {text}$",
    ur"cp\. {greek}; {gloss}, {text}$",
    ur"cp\. {greek} {gloss} in Persia$",
    ur"cp. the adj. {greek} {gloss}; {text}$",
    ur"Skt\. assoc\.$",
    ur"Skt\. assoc\., cp\. {greek}$",
    ur"Skt\. assoc\. in sense of {gloss}$",
    ur"Skt\. {skt} {gloss}$",
    ur"Skt. =Lat\. {latin} {gloss}$",
    ur"IE {pie}, cp\. {greek} {gloss}$",
    ur"Roman cognomen$",
    ur"a Greek name$",
    ur"{text}; {text} {greek} {gloss} {text} {gloss}; {text} {gloss}$",
    ur"later form of {greek}\. IE, cp\. {greek}$",
    ur"etym\. complex, cp\. {text} {gloss}$",
    ur"{greek} \(ἀ- priv\., {greek}\) {gloss}, fr\. {greek}$",
]

compiled_regexes = []

for regex in regexes:
    for name, substitution in regex_templates.items():
        regex = re.sub("{{{}}}".format(name), substitution, regex)
    compiled_regexes.append(re.compile(regex))

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
