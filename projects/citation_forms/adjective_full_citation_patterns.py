#!/usr/bin/env python3

import re
import unicodedata

from morphgnt.utils import load_yaml, sorted_items

from adjective_citation_form_data import ADJECTIVE_CITATION_FORMS

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
}

MOUNCE_OVERRIDES = {
}


def r(s):
    s = re.sub("{art}", "(ὁ|ἡ|το)", s)
    s = re.sub("{V}", "([αεηιουωϊἀὑὠ]|αι|ει)", s)
    return s

first_fail = None
fail_count = 0

for lexeme, metadata in sorted_items(lexemes):
    pos = metadata.get("pos")
    full_citation = metadata.get("full-citation-form")
    dodson_pos = DODSON_OVERRIDES.get(lexeme, metadata.get("dodson-pos", ""))
    mounce_morphcat = MOUNCE_OVERRIDES.get(
        lexeme, metadata.get("mounce-morphcat", ""))

    if (
        pos == "A" or
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

        node = ADJECTIVE_CITATION_FORMS

        # level = 1
        # while node:
        #     success = []
        #     for child in node:
        #         match_tuple, key, children = child
        #         end, cat, dodson = match_tuple
        #         end = r(end)
        #         # print("trying {}".format(key))
        #         if (
        #             re.search(end, strip_accents(full_citation)) and
        #             re.search(cat, mounce_morphcat) and
        #             re.search(dodson, dodson_pos)
        #         ):
        #             success.append((key, children))
        #     if len(success) != 1:
        #         print("testing: {}".format(full_citation))
        #         print("found {} matches at level {}".format(len(success), level))
        #         quit()
        #     node = success[0][1]
        #     level += 1

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
            if not first_fail:
                first_fail = (
                    strip_accents(full_citation),
                    mounce_morphcat,
                    dodson_pos,
                )
                fail_lemma = lexeme
                fail_number = len(success)
            fail_count += 1

if fail_count:
    print(fail_count)
    print("((r\"{}$\",            r\"^{}$\",       r\"^{}$\"), \"\", []),".format(*first_fail))
    print(fail_lemma, fail_number)
