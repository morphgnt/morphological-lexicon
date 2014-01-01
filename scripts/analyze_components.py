#!/usr/bin/env python
# coding: utf-8

import re

from morphgnt.utils import load_yaml, sorted_items

regex_templates = {
    "greek": ur"[\u0370-\u03FF\u1F00-\u1FFF]+",
    "gloss": ur"‘[^’]+’",
    "text": ur"[A-Za-z.,/\- ]+",
    "latin": ur"[A-Za-z]+",
    "pie": ur"\*[a-z]+",
    "skt": ur"[a-zá]+",
    "ref": ur"(?:Mt) \d+:\d+",
}

regexes = [
    ur"s\. prec\.$",
    ur"s\. preceding entry$",
    ur"s\. prec\. {greek}- entries and two next entries$",
    ur"s\. prec\. {greek}- entries; the act\., which is not used in NT ={gloss}$",
    ur"see next entry on the etymology$",
    ur"(orig|etym)\. (complex|not determined|obscure|unclear|uncertain|unknown)$",
    ur"etym\. (complex|unclear|uncertain); {gloss}$",
    ur"etym\. unclear; the NT shows a preference for {greek}$",
    ur"etym\. uncertain; {text}$",
    ur"etym\. uncertain; {text}:{text}$",
    ur"apparently of foreign orig\.$",
    ur"derivation undetermined, but a root signifying {gloss} or {gloss} has claimed attention$",
    ur"Aram\.$",
    ur"Aram\. ={text}; s\. explanation {ref}$",
    ur"Heb\.$",
    ur"Heb\. {gloss}$",
    ur"Heb\., of uncertain etymology$",
    ur"Heb\. name, hence {gloss}$",
    ur"ἀ- priv\., {greek}$",
    ur"ἀ- priv, {greek}$",
    ur"ἀ- priv\., {greek} {gloss}$",
    ur"ἀ- priv\., {greek}; {gloss}$",
    ur"ἀ- priv\., {greek} ={greek} {gloss} {text}; {gloss}$",
    ur"ἀ- priv\., {greek} fr\. {greek}$",
    ur"ἀ- priv\., {greek} {gloss} fr\. {greek}$",
    ur"ἀ- priv\., {greek}, {greek}$",
    ur"ἀ- priv\., {greek}, {greek} {gloss} fr. {greek}$",
    ur"ἀ- priv\., {greek} \({greek}, {greek} {gloss}\) {gloss} or \({greek}, {greek} {gloss} fr\. {greek} {gloss}\) {gloss}$",
    ur"ἀ- priv\., {greek}, q\. v\., in sense of {gloss}; {text}$",
    ur"ἀ- priv\. \(ἁ- by metathesis of aspiration\), {greek}, otherwise a word of uncertain orig\.$",
    ur"ἀ- priv\., {greek}; {text}$",
    ur"ἀ- priv\., {greek}; {gloss}, {text} {gloss} {text}$",
    ur"ἀ- priv\., {greek} {gloss}, freq\. in 3 sg\. {greek}$",
    ur"ἀ- priv\., {greek} {gloss} fr\. {greek}; {gloss}$",
    ur"ἀ- priv\., {greek} {gloss} fr\. {greek}; lit\. {gloss}$",
    ur"ἀ- priv\., cp\. {greek}, {text}$",
    ur"ἀ- priv\., {greek} via 2 aor\. {greek}; {gloss}$",
    ur"ἀ- priv\., {greek}, {greek} {gloss}, cp\. {greek} {gloss}$",
    ur"ἀ\.- priv\., {greek} \(used in the phrase {greek} {greek} {gloss}\) fr\. {greek}$",
    ur"ἀ- priv\., {greek} \({greek}, {greek}\) {gloss}$",
    ur"ἀ- priv\., fr\. {greek} via the fut\. mid\. form of {greek}:{greek}$",
    ur"ἀ- priv\., {greek} =Attic {greek} s$",
    ur"later form of {greek}:ἀ- priv\., {greek} {gloss}$",
    ur"ἀ- copul\., {greek} {gloss}$",
    ur"ἀ- copul\., {greek} {gloss} ={gloss}$",
    ur"ἁ- copul\. {gloss} =Skt\. {skt}-, cp\. {greek} and oblique forms$",
    ur"{greek} \(ἀ- priv\., {greek}\); {gloss} i\. e\. {gloss}$",
    ur"{greek}$",
    ur"{greek} fr\. {greek}$",
    ur"fr\. {text} {greek}$",
    ur"fr\. the fut\. of {greek}, {greek}$",
    ur"={greek}$",
    ur"=ὁ {greek} {gloss}; s\. {greek}$",
    ur"ἡ {greek} {gloss} and ὁ {greek} {gloss}, fr\. a common root:cp\. Lat\. {latin} {gloss}$",
    ur"ὁ {greek} {gloss}$",
    ur"{greek}, originally nt\. pl\. of {greek} with change in accent reflecting emphasis {gloss}; stronger than {greek}$",
    ur"{greek}, {greek} {gloss} \(cp\. {greek}\)$",
    ur"{greek} {gloss}$",
    ur"{greek} {text}$",
    ur"{greek}, {greek} {gloss}$",
    ur"{greek} {gloss}, {greek} {gloss}$",
    ur"{greek} {gloss}, {greek} {gloss}; {text}$",
    ur"{greek}, {greek}$",
    ur"{greek}, {greek}, cp\. {greek} and {greek} {gloss}$",
    ur"{greek} {gloss}, cp\. {greek}$",
    ur"{greek}; {gloss}$",
    ur"{greek}; {gloss}, esp\. {text}$",
    ur"{greek}; any {gloss} or {gloss}$",
    ur"{greek}; only in biblical usage$",
    ur"{greek}; freq\. in ins\. and pap\. of public servants$",
    ur"{greek}, {greek} fr\. {greek}; in later Gk\. {greek} gives way to {greek}$",
    ur"{greek}, {greek}; {text} {gloss}, hence {gloss} and so {gloss}$",
    ur"{greek}; =next entry$",
    ur"{greek} ={greek} \(s\. {greek}\), {greek}$",
    ur"{greek} \(={greek}\); {gloss}$",
    ur"{greek} {gloss} {text}$",
    ur"{greek}, {greek}, {greek} {gloss}$",
    ur"{greek} {gloss} {text}$",
    ur"{greek} {gloss}, {text}$",
    ur"{greek} {gloss}; in non- biblical authors freq\. in sense of {gloss}$",
    ur"{greek} {gloss}, {greek} {gloss} {text} {greek} {gloss}$",
    ur"{greek} {gloss}, mid\. {gloss}$",
    ur"{greek}, {greek} {gloss}, {text}$",
    ur"{greek}, \*{greek}$",
    ur"{greek}; {text}, hence, {gloss}$",
    ur"{greek}, {greek}; {text} {gloss}$",
    ur"{greek}, {greek} {text} ={gloss}$",
    ur"{greek}, {greek} {gloss} formed from the fut\. of {greek}, the compound fr\. {greek}$",
    ur"{greek}; {gloss}; cp\. {greek} {text} {gloss}$",
    ur"{greek}, {greek} {gloss}; prim\. {gloss}, {text}$",
    ur"{greek}, {greek}; prim\. {gloss} then {gloss}, {text}$",
    ur"{greek}, {greek}; prim\. a commercial term$",
    ur"{greek}, {greek} {gloss}, cp\. {greek}; {gloss}, hence {gloss}$",
    ur"{greek} {gloss} fr\. {greek} a later form of {greek}$",
    ur"{greek}, {greek}; in non- biblical Gk\. {greek} in this word signifies {gloss}; {gloss} ={gloss}$",
    ur"{greek}, {greek} {gloss}, cp\. {greek}; {text}$",
    ur"{greek}, {greek}; various senses in non- bibl\. Gk\.$",
    ur"{greek}; {text}$",
    ur"{greek} {gloss}; prim\. {gloss} esp\. as {gloss} {text}$",
    ur"{greek}, cp\. {greek} \({greek}, {greek}\) {gloss}$",
    ur"{greek}, {greek}; {text}$",
    ur"{greek}, {greek}; {gloss} {text}$",
    ur"{greek}, {greek} via the mid\.$",
    ur"{greek}, {greek} {gloss} fr\. {greek}$",
    ur"{greek}, {greek} {gloss}; {gloss}$",
    ur"{greek}, {greek} via {greek} {gloss}, in various senses, including {text} as {gloss} and {gloss}$",
    ur"{greek}, {greek}; {gloss}, e\. g\. {text}$",
    ur"s\. {greek}$",
    ur"later form of {greek} in same sense$",
    ur"{greek} \({greek} and {greek} via the aor\. pass\. inf\. {greek}\)$",
    ur"=Attic {greek}$",
    ur"Attic form of {greek}$",
    ur"Attic form ={greek}, etym\. uncertain$",
    ur"assoc. w. {greek}; {gloss}, also {gloss}$",
    ur"assoc. w. {greek} {text}, pl\. as in {greek} {gloss}$",
    ur"for older {greek}$",
    ur"in older Gk\. also {greek}$",
    ur"freq\. as v\. l\. for {greek}$",
    ur"by- form of {greek}$",
    ur"by- form of {greek}; {gloss}$",
    ur"by- form of {greek} \({greek}, {greek} {gloss}\)$",
    ur"{greek} {gloss}, {greek}; {text}$",
    ur"{greek} {gloss}, {greek}; {gloss}, {text}$",
    ur"{greek}, {greek} {gloss}, as compound fr\. {greek}$",
    ur"{greek}, {greek} {gloss} also {gloss}, as compound fr\. {greek}$",
    ur"{greek}, {greek}; {gloss}$",
    ur"folk- etymology \(ἀ- priv\., {greek}\) underlies the Gk\. formation of this foreign word, suggesting perh\. {gloss}$",
    ur"cp\. {greek}$",
    ur"cp\. {greek} {gloss}$",
    ur"cp\. {greek}; {gloss}$",
    ur"cp\. {greek} {gloss} and {greek}$",
    ur"cp\. {greek} {gloss}, {text}; cp\. our {gloss} in ref\. to {text}$",
    ur"cp\. {greek}; {gloss}, {text}$",
    ur"cp\. {greek} {gloss} in Persia$",
    ur"cp\. the adj. {greek} {gloss}; {text}$",
    ur"cp\. epic noun {greek} and Attic {greek}, both {gloss}$",
    ur"cp\. the epic form {greek} {gloss}; rare in the nt\. form$",
    ur"cp\. Lat\. {latin}$",
    ur"cp\. Lat\. {latin} {gloss}$",
    ur"cp\. Lat\. {latin} {gloss}; in the strict sense:{text}; the synonym {greek} in the strict sense refers to {gloss} or {gloss}, {text}. Usage in the NT is much more fluid.$",
    ur"Lat\. {latin} {gloss}; {gloss}; {text}$",
    ur"Skt\. assoc\.$",
    ur"Skt\. via Heb\.$",
    ur"Skt\. assoc\., cp\. {greek}$",
    ur"Skt\. assoc\. in sense of {gloss}$",
    ur"Skt\. {skt} {gloss}$",
    ur"Skt\. {skt} · {gloss}$",
    ur"Skt. =Lat\. {latin} {gloss}$",
    ur"IE$",
    ur"IE; mostly used by poets$",
    ur"IE {pie}, cp\. {greek} {gloss}$",
    ur"IE; {text}:{text}$",
    ur"IE; var\. senses in Gk\. lit\.$",
    ur"IE, cp\. Lat\. {latin}$",
    ur"Roman cognomen$",
    ur"a Greek name$",
    ur"{text}; {text} {greek} {gloss} {text} {gloss}; {text} {gloss}$",
    ur"later form of {greek}\. IE, cp\. {greek}$",
    ur"later word for {greek} and freq\. w\. {greek} as v\. l\.$",
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
