#!/usr/bin/env python3

import re
import unicodedata

from morphgnt.utils import load_yaml, sorted_items

from citation_form_data import CITATION_FORMS

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

    ## problematic without changes to lexemes.yaml or morphgnt

    "αἴτιον",  # adj.
    "ἀκμήν",  # adv.
    "ἀλάβαστρος",
    "ἀμήτωρ",  # adj.
    "ἀπάτωρ",  # adj.
    "ἀπελεύθερος",  # adj.
    "ἅρπαξ",  # adj.
    "αὐτόχειρ",  # adj.
    "Βαριησοῦς",
    "Βαριωνᾶ",
    "βάτος",
    "βοηθός",  # adj.
    "Γαλιλαῖος",  # adj.
    "Γερασηνός",  # adj.
    "δοῦλος",
    "Ἑβραΐς",  # danker gives noun citation form but morphgnt has as adj.
    "ἔγγυος",  # adj.
    "ἔγκυος",  # adj.
    "ἔρημος",  # adj.
    "ζῆλος",
    "ἦχος",
    "θρίξ",
    "ἱερόν",  # danker gives noun citation form but morphgnt has as adj.
    "Ἱεροσόλυμα",
    "ἱερόσυλος",  # adj.
    "ἱλαστήριον",  # danker gives noun citation form but morphgnt has as adj.
    "Ἰσκαριώτης",
    "Ἰωβήλ",
    "λεγιών",
    "λεπτόν",
    "μέλαν",
    "μίσθιος",
    "μισθωτός",  # danker gives noun citation form but morphgnt has as adj.
    "μοιχαλίς",  # danker gives noun citation form but morphgnt has as adj.
    "Μωϋσῆς",
    "νῆστις",  # danker gives noun citation form but morphgnt has as adj.
    "πανοῦργος",
    "παράσημος",
    "πένης",  # danker gives noun citation form but morphgnt has as adj.
    "πετεινόν",  # danker gives noun citation form but morphgnt has as adj.
    "πλανήτης",  # danker gives noun citation form but morphgnt has as adj.
    "πλατεῖα",  # danker gives noun citation form but morphgnt has as adj.
    "πρόγονος",
    "Σαλείμ",
    "Σολομών",
    "στεῖρα",  # danker gives noun citation form but morphgnt has as adj.
    "σύζυγος",  # danker gives noun citation form but morphgnt has as adj.
    "συνεργός",  # danker gives noun citation form but morphgnt has as adj.
    "Ταρσός",
    "τιμιότης",
    "Τραχωνῖτις",  # danker gives noun citation form but morphgnt has as adj.
    "χήρα",  # danker gives noun citation form but morphgnt has as adj.

    ##

    "ἄκων", "ἀμήτωρ", "ἀνθρωποκτόνος", "ἀπάτωρ", "ἀπελεύθερος", "ἄραφος",
    "Ἄρειος", "ἅρπαξ", "αὐτόχειρ", "δεῖνα", "δέκα", "δεκαοκτώ", "δεκαπέντε",
    "δεκατέσσαρες", "δύο", "δώδεκα", "ἑβδομήκοντα", "Ἑβραῖος", "Ἑβραΐς",
    "ἑδραῖος", "εἴκοσι(ν)", "εἷς", "ἑκατόν", "ἐλάσσων", "ἐλωΐ", "ἕνδεκα",
    "ἐνενήκοντα", "ἐννέα", "ἕξ", "ἑξήκοντα", "ἑπτά", "εὐθύς", "ἠλί", "ἱερόν",
    "ἱλαστήριον", "ἵλεως", "κακοποιός", "Καλός", "Κορίνθιος", "κόσμιος",
    "λοίδορος", "λοιμός", "μέγας", "μέγιστος", "μείζων", "μέλας", "μηδείς",
    "μισθωτός", "μοιχαλίς", "νεκρός", "νῆστις", "ὀγδοήκοντα", "οἰκεῖος",
    "ὀκτώ", "οὐδείς", "παρείσακτος", "παρόμοιος", "πᾶς", "πάσχα", "πένης",
    "πέντε", "πεντήκοντα", "πετεινόν", "Πισιδία", "πλανήτης", "πλατεῖα",
    "πολύς", "πραΰς", "πτηνόν", "ραββουνι", "ῥακά", "σκυθρωπός", "σπερμολόγος",
    "στεῖρα", "σύζυγος", "συναιχμάλωτος", "συνεργός", "σύντροφος", "ταλιθα",
    "τέσσαρες", "τεσσεράκοντα", "Τραχωνῖτις", "Τρεῖς", "τρεῖς", "τριάκοντα",
    "ὑγιής", "χήρα",

    ## additional ones without full-citation

    "ἀλλήλων",
    "αὐτός",
    "ἑαυτοῦ",
    "ἐγώ",
    "ἐκεῖνος",
    "ἐμαυτοῦ",
    "ἐμός",
    "ἔοικα",
    "ἡλίκος",
    "ἡμέτερος",
    "κἀγώ",
    "κἀκεῖνος",
    "μακρός",
    "ὁ",
    "ὅδε",
    "οἷος",
    "ὁποῖος",
    "ὅς",
    "ὅσος",
    "ὅστις",
    "οὗτος",
    "παραπλήσιον",
    "πηλίκος",
    "ποῖος",
    "πόσος",
    "ποταπός",
    "πρότερος",
    "πρῶτος",
    "πυκνά",
    "σεαυτοῦ",
    "σός",
    "σύ",
    "τηλικοῦτος",
    "τις",
    "τίς",
    "τοιόσδε",
    "τοιοῦτος",
    "τοσοῦτος",
    "ὑμέτερος",

    ## other problematic examples

    "αἴτιον",
    "βοηθός",
    "Γαλιλαῖος",
    "Γερασηνός",
    "δεισιδαίμων",
    "δοῦλος",
    "ἔγγυος",
    "ἔγκυος",
    "ἔρημος",
    "ἱερόσυλος",
    "μέλαν",
    "μίσθιος",
    "οἰκιακός",
    "πανοῦργος",
    "παραλυτικός",
    "παράσημος",
    "πρόγονος",
    "συγγενίς",
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

    "ἅλα":           "N:N",
    "Ἄψινθος":       "N:M",
    "δύσις":         "N:F",
    "Ἰουνία":        "N:F",
    "Μαθθαῖος":      "N:M",
    "Μαθθίας":       "N:M",
    "μητρολῴας":     "N:M",
    "σκῦλα":         "N:N",
    "στάδιος":       "N:M",
    "ψίξ":           "N:F",
}

MOUNCE_OVERRIDES = {
    "Ἀθῆναι":       "n-1c",

    "ζυγός":        "n-2a",
    "ἄψινθος":      "n-2b",
    "Πέργαμος":     "n-2b",

    "θάμβος":       "n-3d(2b)",
    "στάχυς":       "n-3e(1)",

    "ἅλα":          "n-3c(6d)",
    "Ἄψινθος":      "n-2a",
    "δεσμόν":       "n-2c",
    "δύσις":        "n-3e(5b)",
    "θέρμη":        "n-1b",
    "Ἰουνία":       "n-1a",
    "Μαθθαῖος":     "n-2a",
    "Μαθθίας":      "n-1d",
    "μητρολῴας":    "n-1d",
    "νουμηνία":     "n-1a",
    "νύμφη":        "n-1b",
    "σκῦλα":        "n-2c",
    "στάδιος":      "n-2a",
    "τριετία":      "n-1a",
    "χείμαρρος":    "n-2a",
    "ψίξ":          "n-3b(3)",

    "ἁλληλουϊά":        "x-indecl",
    "δέκα":             "a-indecl",
    "δεκαοκτώ":         "a-indecl",
    "δεκαπέντε":        "a-indecl",
    "δεκατέσσαρες":     "a-indecl",
    "δώδεκα":           "a-indecl",
    "ἑβδομήκοντα":      "a-indecl",
    "ἑβδομηκοντάκις":   "d-indecl",
    "εἴκοσι(ν)":        "a-indecl",
    "ἑκατόν":           "a-indecl",
    "ἕνδεκα":           "a-indecl",
    "ἐνενήκοντα":       "a-indecl",
    "ἐννέα":            "a-indecl",  # danker has citation form with articles
    "ἕξ":               "a-indecl",
    "ἑξήκοντα":         "a-indecl",
    "ἑπτά":             "a-indecl",
    "εφφαθα":           "v-indecl",
    "κουμ":             "v-indecl",
    "λεμά":             "d-indecl",
    "ὀγδοήκοντα":       "a-indecl",
    "ὀκτώ":             "a-indecl",
    "παραλυτικός":      "a-?",
    "πέντε":            "a-indecl",
    "πεντήκοντα":       "a-indecl",
    "σαβαχθάνι":        "v-indecl",
    "τεσσεράκοντα":     "a-indecl",
    "τριάκοντα":        "a-indecl",
    "ὡσαννά":           "x-indecl",
}


def r(s):
    s = re.sub("{art}", "(ὁ|ἡ|το)", s)
    s = re.sub("{V}", "([αεηιουωϊἀὑὠ]|αι|ει)", s)
    return s


fail_count = 0

for lexeme, metadata in sorted_items(lexemes):
    pos = metadata.get("pos")
    full_citation = metadata.get("full-citation-form")
    dodson_pos = DODSON_OVERRIDES.get(lexeme, metadata.get("dodson-pos", ""))
    mounce_morphcat = MOUNCE_OVERRIDES.get(
        lexeme, metadata.get("mounce-morphcat", ""))

    if (
        (pos == "N") or
        (dodson_pos and dodson_pos.startswith("N")) or
        (
            isinstance(mounce_morphcat, str) and
            mounce_morphcat.startswith("n")
        ) or (
            isinstance(mounce_morphcat, list) and
            any(x.startswith("n") for x in mounce_morphcat)
        ) or
        (pos == "A") or
        (dodson_pos and dodson_pos == "A") or
        (
            isinstance(mounce_morphcat, str) and
            mounce_morphcat.startswith("a-")
        ) or (
            isinstance(mounce_morphcat, list) and
            any(x.startswith("a-") for x in mounce_morphcat)
        )
    ):

        if lexeme in SKIP:
            continue

        if isinstance(mounce_morphcat, list):
            mounce_morphcat = ";".join(mounce_morphcat)

        node = CITATION_FORMS

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
                if fail_count == 0:
                    print("testing: {}".format(full_citation))
                    print(lexeme)
                    print(mounce_morphcat)
                    print(dodson_pos)
                    print("found {} matches at level {}".format(len(success), level))
                fail_count += 1
                break
            node = success[0][1]
            level += 1

print(fail_count)
