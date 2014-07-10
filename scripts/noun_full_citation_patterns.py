#!/usr/bin/env python3

import re
import unicodedata

from morphgnt.utils import load_yaml, sorted_items

from noun_citation_form_data import NOUN_CITATION_FORMS

lexemes = load_yaml("lexemes.yaml")

ACUTE = u"\u0301"
GRAVE = u"\u0300"
CIRCUMFLEX = u"\u0342"


def strip_accents(w):
    return "".join(
        unicodedata.normalize("NFC", "".join(
            component
            for component in unicodedata.normalize("NFD", ch)
            if component not in [ACUTE, GRAVE, CIRCUMFLEX]
        )) for ch in w
    )

SKIP = [

    ## missing full citation

    "αἴτιον",
    "ἀκμήν",
    "ἁλληλουϊά",
    "ἀμήτωρ",
    "ἀπάτωρ",
    "ἀπελεύθερος",
    "ἅρπαξ",
    "αὐτόχειρ",
    "βοηθός",
    "Γαλιλαῖος",
    "Γερασηνός",
    "δέκα",
    "δεκαοκτώ",
    "δεκαπέντε",
    "δεκατέσσαρες",
    "δώδεκα",
    "ἑβδομήκοντα",
    "ἑβδομηκοντάκις",
    "Ἑβραΐς",
    "ἔγγυος",
    "ἔγκυος",
    "εἴκοσι(ν)",
    "ἑκατόν",
    "ἕνδεκα",
    "ἐνενήκοντα",
    "ἐννέα",
    "ἕξ",
    "ἑξήκοντα",
    "ἑπτά",
    "ἔρημος",
    "εφφαθα",
    "ἱερόν",
    "ἱερόσυλος",
    "ἱλαστήριον",
    "κουμ",
    "λεμά",
    "λεπτόν",
    "μίσθιος",
    "μισθωτός",
    "μοιχαλίς",
    "νῆστις",
    "ὀγδοήκοντα",
    "ὀκτώ",
    "πανοῦργος",
    "παραλυτικός",
    "παράσημος",
    "πένης",
    "πέντε",
    "πεντήκοντα",
    "πετεινόν",
    "πλανήτης",
    "πλατεῖα",
    "πρόγονος",
    "σαβαχθάνι",
    "στεῖρα",
    "σύζυγος",
    "συνεργός",
    "τεσσεράκοντα",
    "Τραχωνῖτις",
    "τριάκοντα",
    "χήρα",
    "ὡσαννά",

    ## missing mounce-morphcat

    "ἅλα",
    "ἀλάβαστρος",
    "Ἄψινθος",
    "βάτος",
    "δεσμόν",
    "δύσις",
    "ἦχος",
    "θέρμη",
    "Ἰουνία",
    "Ἰωβήλ",
    "Μαθθαῖος",
    "Μαθθίας",
    "μητρολῴας",
    "νουμηνία",
    "νύμφη",
    "Σαλείμ",
    "σκῦλα",
    "στάδιος",
    "τριετία",
    "χείμαρρος",
    "ψίξ",

    ## problematic without changes to lexemes.yaml

    "δοῦλος",
    "θρίξ",
    "Ἱεροσόλυμα",
    "Ἰσκαριώτης",
    "μέλαν",
    "Μωϋσῆς",
    "Σολομών",
    "ζῆλος",
    "τιμιότης",
    "Ταρσός",
    "Βαριησοῦς",
    "λεγιών",
    "Βαριωνᾶ",
]

DODSON_OVERRIDES = {
    "ἀφθορία":       "N:F",
    "δοκιμασία":     "N:F",
    "εἰδέα":         "N:F",
    "οἰκετεία":      "N:F",
    "ὀλιγοπιστία":   "N:F",
    "πραϋπαθία":     "N:F",
    "Εὕα":           "N:F",
    "κοπρία":        "N:F",
    "Μαρία":         "N:F",

    "βελόνη":        "N:F",
    "διαπαρατριβή":  "N:F",
    "ἐμπαιγμονή":    "N:F",
    "καταδίκη":      "N:F",
    "ὁμίχλη":        "N:F",

    "κορβανᾶς":      "N:M",

    "Ζηλωτής":       "N:M",
    "προσαίτης":     "N:M",
    "στασιαστής":    "N:M",

    "ἄμωμον":        "N:N",  # but Heb 9.14
    "ἀνάγαιον":      "N:N",
    "κλινάριον":     "N:N",
    "κόπριον":       "N:N",
    "σιτίον":        "N:N",
    "φάρμακον":      "N:N",
    "ὠτάριον":       "N:N",
    "δυσεντέριον":   "N:N",
    "Σόδομα":        "N:N",
    "στάδιον":       "N:N",

    "ἀνθρωποκτόνος": "N:M",
    "Ἑβραῖος":       "N:M",
    "ἑκατόνταρχος":  "N:M",
    "ἐλεγμός":       "N:M",
    "Καναναῖος":     "N:M",
    "Κορίνθιος":     "N:M",
    "κυλισμός":      "N:M",
    "λοίδορος":      "N:M",
    "νοσσός":        "N:M",
    "οἰκιακός":      "N:M",
    "οἰκοδόμος":     "N:M",
    "Πύρρος":        "N:M",
    "συναιχμάλωτος": "N:M",
    "Τίτιος":        "N:M",
    "σῖτος":         "N:M",

    "ἄψινθος":       "N:F",

    "δισμυριάς":     "N:F",
    "στιβάς":        "N:F",
    "συγγενίς":      "N:F",
    "διόρθωμα":      "N:N",
    "τρῆμα":         "N:N",
    "ὑπόλειμμα":     "N:N",
    "ἄγγος":         "N:N",
    "δέος":          "N:N",
    "ἐκζήτησις":     "N:F",
    "ἔλεος":         "N:N",
    "ἐπίστασις":     "N:F",
    "λῆμψις":        "N:F",
    "μετάλημψις":    "N:F",
    "πρόσκλισις":    "N:F",
    "σκότος":        "N:N",
    "εὐρακύλων":     "N:M",
    "Σαρών":         "N:M",
    "κατήγωρ":       "N:M",
    "προπάτωρ":      "N:M",
}

MOUNCE_OVERRIDES = {
    "Ἀθῆναι":       "n-1c",

    "ζυγός":        "n-2a",
    "ἄψινθος":      "n-2b",
    "Πέργαμος":     "n-2b",

    "θάμβος":       "n-3d(2b)",
    "στάχυς":       "n-3e(1)",
}


def r(s):
    s = re.sub("{art}", "(ὁ|ἡ|το)", s)
    s = re.sub("{V}", "([αεηιουωϊἀὑὠ]|αι|ει)", s)
    return s


for lexeme, metadata in sorted_items(lexemes):
    pos = metadata.get("pos")
    full_citation = metadata.get("full-citation-form")
    dodson_pos = DODSON_OVERRIDES.get(lexeme, metadata.get("dodson-pos", ""))
    mounce_morphcat = MOUNCE_OVERRIDES.get(
        lexeme, metadata.get("mounce-morphcat", ""))

    if (
        pos == "N" or
        (dodson_pos and dodson_pos.startswith("N")) or
        (
            isinstance(mounce_morphcat, str) and
            mounce_morphcat.startswith("n")
        ) or (
            isinstance(mounce_morphcat, list) and
            any(x.startswith("n") for x in mounce_morphcat)
        )
    ):

        if lexeme in SKIP:
            continue

        if not re.match(r"(\w+), (\w+), (\w+)$", full_citation):
            continue

        if isinstance(mounce_morphcat, list):
            mounce_morphcat = ";".join(mounce_morphcat)

        node = NOUN_CITATION_FORMS

        level = 1
        while node:
            success = []
            for child in node:
                match_tuple, key, children = child
                end, cat, dodson = match_tuple
                end = r(end)
                # print("trying {}".format(key))
                if (
                    re.search(end, strip_accents(full_citation)) and
                    re.search(cat, mounce_morphcat) and
                    re.search(dodson, dodson_pos)
                ):
                    success.append((key, children))
            if len(success) != 1:
                print("testing: {}".format(full_citation))
                print("found {} matches at level {}".format(len(success), level))
                quit()
            node = success[0][1]
            level += 1
