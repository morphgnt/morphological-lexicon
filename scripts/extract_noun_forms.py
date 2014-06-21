#!/usr/bin/env python3

from collections import defaultdict

from morphgnt.utils import load_yaml, load_wordset, sorted_items
from morphgnt import filesets

lexemes = load_yaml("lexemes.yaml")
indeclinables = load_wordset("nominal-indeclinable.txt")

SKIP = [
    "ἄγαμος",
    "ἀλάβαστρος",
    "ἅλα",
    "ἄρκος",
    "βάτος",
    "γείτων",
    "διάκονος",
    "θεός",
    "θυρωρός",
    "κάμηλος",
    "κοινωνός",
    "λιμός",
    "ὄνος",
    "ὄρνις",
    "παῖς",
    "παρθένος",
    "Πάτμος",
    "στάμνος",
    "ὕαλος",
    "ὕσσωπος",
    "πλοῦτος",
    "ζῆλος",
    "ἀλάβαστρον",
    "Ἅννα",
    "Ἅννας",
    "Μανασσῆ",
    "Ἱεροσόλυμα",
    "Ἀπολλῶ",
    "ἄψινθος",
    "Ἄψινθος",
    "ἦχος",
    "κακοποιός",
    "σκῦλα",
    "στάδιος",
    "τοὐναντίον",
    "τοὔνομα",
    "χείρ",
    "Καῦδα",
    "ἑκατοντάρχης",  # @@@ fix lemma in sblgnt
    "Μανασσῆς",
    "Ἀπολλῶς",
    "Κώς",
    "ἔρις",  # n-3e(5b) some of the time?
    "κλείς",  # also mixed class
    "γάλα",
    "γόνυ",
    "κρέας",
    "μέλι",
    "δάκρυον",
    "σάββατον",
    "τιμιότης",
    "Γόμορρα",
    "γυνή",
]

MOUNCE_OVERRIDES = {
    "Ἰουνία": "n-1a",
    "τριετία": "n-1a",
    "νύμφη": "n-1b",
    "δεῖνα": "n-3f(1a)",
    "Ἰσκαριώτης": "n-1f",
    "Μαθθαῖος": "n-2a",
    "Μαθθίας": "n-1d",
    "μήν": "n-3f(1a)",
    "δεσμόν": "n-2c",
    "δύσις": "n-3e(5b)",
    # "ἦχος": ["n-2a", "n-3d(2)"],
    "θέρμη": "n-1b",
    # "κακοποιός": "a-3a",
    "μέλαν": "n-3f(1a)",
    "μητρολῴας": "n-1d",
    "νουμηνία": "n-1a",
    "χείμαρρος": "n-2a",
    "ζυγός": "n-2a",
    "στάχυς": "n-3e(1)",
    "Πέργαμος": "n-2b",
    "θάμβος": "n-3d(2b)",
    "ὀστέον": "n-2d",
    "βάθος": "n-3d(2b)",
    "ἐξανάστασις": "n-3e(5b)",
}

fs = filesets.load("filesets.yaml")

# form -> set(cng)
forms = defaultdict(set)

# form -> set(mounce)
cats = defaultdict(set)

# form -> count
counts = defaultdict(int)


for row in fs["sblgnt-lexemes"].rows():
    lemma = row["lemma"]
    norm = row["norm"]

    if row["ccat-pos"] == "N-":
        if lemma in indeclinables:
            continue
        if row["ccat-parse"][4] == "V":
            continue
        if lemma in SKIP:
            continue

        if lemma in MOUNCE_OVERRIDES:
            mounce = MOUNCE_OVERRIDES[lemma]
        elif lemma in lexemes and "mounce-morphcat" in lexemes[lemma]:
            mounce = lexemes[lemma]["mounce-morphcat"]
        else:
            mounce = ""

        if mounce == "n-3g(1)":
            continue

        if not isinstance(mounce, list):
            mounce = [mounce]
        for cat in mounce:
            if cat.startswith("n-"):
                cats[norm].add(cat)

        parse = row["ccat-parse"][4:7]
        forms[norm].add(parse)
        counts[norm] += 1

        # syncretism

        if parse[2] == "N":
            if parse[0] == "N":
                forms[norm].add("A" + parse[1:])
            if parse[0] == "A":
                forms[norm].add("N" + parse[1:])
        if "n-1a" in mounce:
            if parse == "APF":
                forms[norm].add("GSF")
            if parse == "GSF":
                forms[norm].add("APF")
        if "n-1d" in mounce:
            if parse == "NSM":
                forms[norm].add("APM")
            if parse == "APM":
                forms[norm].add("NSM")
        if "n-3e(3)" in mounce or "n-3e(5b)" in mounce:
            if parse[:2] == "AP":
                forms[norm].add("NP" + parse[2])
            if parse[:2] == "NP":
                forms[norm].add("AP" + parse[2])


for form, data in sorted_items(forms):
    if cats[form]:
        cat_string = ":".join(cats[form])
    else:
        cat_string = "@@@"
    print("{}|{}|{}|{}".format(
        form, cat_string, ":".join(sorted(data)), counts[form]))
