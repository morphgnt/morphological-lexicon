#!/usr/bin/env python3

from pysblgnt import morphgnt_rows
from pyuca import Collator
import yaml

from characters import strip_accents

from collections import defaultdict
import re

IGNORE_LIST = [
    "ῥαββί",
    "ἰῶτα",  # @@@
    "ἠλί",
    "ταλιθα",
    "ραββουνι",
    "αββα",
    "ἐλωΐ",
    "πάσχα",
    "μαράνα",
    "μάννα",
    "ῥακά",
    "σίκερα",
    "δεκατέσσαρες",
    "τεσσεράκοντα",
    "δύο",
    "δώδεκα",
    "ἑπτά",
    "ἑκατόν",
    "ἑξήκοντα",
    "τριάκοντα",
    "πέντε",
    "ἕξ",
    "ἐνενήκοντα",
    "ἐννέα",
    "δέκα",
    "ἕνδεκα",
    "πεντήκοντα",
    "ὀκτώ",
    "ὀγδοήκοντα",
    "δεκαοκτώ",
    "εἴκοσι(ν)",
    "δεκαπέντε",
    "ἑβδομήκοντα",

    "ὅδε",
    "τοιόσδε",

    # not in lexemes.yaml
    "μήν",

    "γυνή",
    "θρίξ",
    "θυγάτηρ",
    "ἔρις",
    "κλείς",
    "ὀστέον",
    "οὖς",  # needs to be distinguished from fws
    "χείρ",  # just problematic in DPF
    "χάρις",  # just problematic in ASF

    "πολύς",
    "μέγας",

    "ὅσιος", # need to sort out 150208
    "νηφάλιος",
    "μάταιος",
    "ἥμισυς",  # what's going on in GSN?

    "τρεῖς",  # works but revisit (p236)
    "οὐδείς",
    "εἷς",
    "μηδείς",

    "τέσσαρες",

    "ὁ",
    "ὅς",
    "οὗτος",
    "αὐτός",
    "ὅστις",
    "τοιοῦτος",
    "ἐκεῖνος",
    "ἄλλος",
    "τοσοῦτος",
    "ἑαυτοῦ",
    "σεαυτοῦ",
    "κἀκεῖνος",
    "ἀλλήλων",
    "τηλικοῦτος",

    "παραπλήσιον",

    "ἑκατοντάρχης",  # @@@ lemmatization bug?
    "πλοῦτος",
]

MOUNCE_OVERRIDES = {
    "ἄγαμος": "n=2a/2b",
    "αἴτιον": "a-1a(1)",  # should it be αἴτιος?
    # "ἀκριβέστερον",
    "ἄκων": "a-2a(2)",
    "ἅλα": "n-3c(6aALA)",  # @@@
    "ἀλάβαστρος": "n-2b",
    # "ἀλυπότερος",
    "ἀμφιέννυμι": "v-3c(1)",
    # "ἀνάθεμα",  # @@@ lemmatization bug?
    # "ἀνώτερος",
    "ἄπειμι": "cv-6b",
    "ἄψινθος": "n-2b",
    "βάθος": "n-3d(2b)",
    "βασίλειον": "a-3a",  # should it be βασίλειος in Luke?
    "βάτος": "n=2a/2b",
    # "βέλτιον",
    "δάκρυον": "n=2c(SIN)",  # n-2c with σι(ν) DPN
    "δεῖνα": "n-3f(1a)",
    "δεκάτη": "a-1a(2a)",  # should it be δέκατος
    "δεσμόν": "n-2c",
    "διάκονος": "n=2a/2b",
    "διαπλέω": "cv-1a(7)",
    "δοῦλος": "a-1a(2a)",  # @@@
    "δύσις": "n-3e(5b)",
    "εἰδωλόθυτον": "a-3a",  # should it be εἰδωλόθυτος ?
    "εἴωθα": "v-1b(3)",
    "ἑκών": "a-2a(2)",  # made up subcategory to select n-3c(5b) in masculine/neuter
    "ἔννυχα": "a-3a",  # incorrect lemma?
    "ἐξανάστασις": "n-3e(5b)",
    "ἐξανάστασις": "n-3e(5b)",
    "ἔρημος": "a-3a",
    "ἔσθω": "v-1b(3)",
    "ἑτεροζυγέω": "v-1d(2a)",
    # "εὐκοπώτερος",
    "εὐπάρεδρον": "a-3a",  # should it be εὐπάρεδρος?
    "ζῆλος": "n=2a/3d(2)",
    "ζυγός": "n-2a",
    # "ἥδιστα",
    "ἦχος": ["n=2a/3d(2)"],
    # "θάμβος",  # n-2a but neut
    "θάμβος": "n-3d(2b)",
    "θεός": "n=2a/2b",
    "θέρμη": "n-1b",
    "θυρωρός": "n=2a/2b",
    "Ἰουνία": "n-1a",
    "ἱππικόν": "a-1a(2a)",  # should it be ἱππικός?
    "Ἰσκαριώτης": "n-1f",
    "κακοποιός": "a-3a",
    "κάμηλος": "n-2b",
    "λεπτόν": "a-1a(2a)",  # @@@ lemma?
    "λιμός": "n=2a/2b",
    "Μαθθαῖος": "n-2a",
    "Μαθθίας": "n-1d",
    "μέλαν": "a-2a(3)",  # made up subcategory
    "μήν": "n-3f(1a)",
    "μητρολῴας": "n-1d",
    "μίγνυμι": "v-3c(2)",
    "νουμηνία": "n-1a",
    "νύμφη": "n-1b",
    "οἶμαι": "v-1d(2c)",
    "ὄνος": "n=2a/2b",  # masculine in Luke
    "ὀστέον": "n-2d",
    "ὀψία": "n-1a",
    "παρθένος": "n=2a/2b",  # only masculine in Revelation
    "παρίστημι": "cv-6a",
    "Πέργαμος": "n-2b",
    "πυκνά": "a-1a(2a)",  # change to πυκνός in Luke?
    "σάββατον": "n=2c(SAB)",  # n-2c with σι(ν) DPN
    "σκῦλα": "n-2c",  # change to σκῦλον?
    "στάδιος": "n-2a",
    "στάμνος": "n-2b",
    "στάχυς": "n-3e(1)",
    "συνομιλέω": "cv-1d(2a)",
    # "τάχιον",
    "ταχύ": "adverb",
    "τέσσαρες": "a-4c",
    "τιμιότης": "n-3c(1)",
    # "τομώτερος",
    "τοὔνομα": "n-3c(4)",
    "τριετία": "n-1a",
    "τρίμηνον": "a-3a",  # should it be τρίμηνος?
    "ὕαλος": "n-2a",
    # "ὕστερον",
    "φοβέομαι": "v-1d(2a)", # ?
    "χείμαρρος": "n-2a",
    "χρύσεος": "a-1b",  # should it be χρύσους?
    "ψίξ": "n-3b(3)",
}

forms_by_lemma = defaultdict(lambda: defaultdict(lambda: defaultdict(set)))
mounce_by_lemma = defaultdict(set)
theme_by_lemma = defaultdict(lambda: defaultdict(set))

stems_and_class_by_lemma = defaultdict(lambda: defaultdict(lambda: defaultdict(set)))

with open("nominal_endings.yaml") as f:
    noun_endings = yaml.load(f)

with open("../morphological-lexicon/lexemes.yaml") as f:
    lexemes = yaml.load(f)

for book_num in range(1, 28):
    for row in morphgnt_rows(book_num):
        ccat_pos = row["ccat-pos"]
        ccat_parse = row["ccat-parse"]
        norm = row["norm"]
        lemma = row["lemma"]

        if norm == "πειθοῖ(ς)":
            norm = "πειθοῖς"  # @@@

        if ccat_parse[4] == "-":
            continue

        if ccat_parse[7] != "-":
            continue  # @@@

        if lemma in IGNORE_LIST:
            continue

        if lemma[0].lower() != lemma[0]:
            continue

        if lemma in MOUNCE_OVERRIDES:
            mounce_cat = MOUNCE_OVERRIDES[lemma]
        else:
            lexeme = lexemes[lemma]
            try:
                mounce_cat = lexeme["mounce-morphcat"]
            except:
                print("{} has no mounce-morphcat".format(lemma))
                quit()
        if not isinstance(mounce_cat, list):
            mounce_cat = [mounce_cat]

        case_number = ccat_parse[4:6]
        gender = ccat_parse[6]
        aspect_voice = ccat_parse[1:3]
        if aspect_voice == "PP":
            aspect_voice = "PM"
        if aspect_voice == "XP":
            aspect_voice = "XM"

        for cat in mounce_cat:
            mounce_by_lemma[lemma].add(cat)

        new_mounce_cat = []
        for cat in mounce_cat:
            if cat == "a-1a(1)":
                if gender == "M":    cat = "n-2a"
                elif gender == "F":  cat = "n-1a"
                elif gender == "N":  cat = "n-2c"
                else: assert False
            elif cat == "a-1a(2a)":
                if gender == "M":    cat = "n-2a"
                elif gender == "F":  cat = "n-1b"
                elif gender == "N":  cat = "n-2c"
                else: assert False
            elif cat == "a-1a(2b)":
                pass
            elif cat == "a-1b":
                if gender == "M":    cat = "n-2d"
                elif gender == "F":  cat = "n-1h"
                elif gender == "N":  cat = "n-2d"
                else: assert False
            elif cat == "a-2a":
                if gender == "M":    cat = "n-3c(5a)"
                elif gender == "F":  cat = "n-1c"
                elif gender == "N":  cat = "n-3c(5a)"
                else: assert False
            elif cat == "a-2a(2)":  # made up
                if gender == "M":    cat = "n-3c(5b)"
                elif gender == "F":  cat = "n-1c"
                elif gender == "N":  cat = "n-3c(5b)"
                else: assert False
            elif cat == "a-2a(3)":  # made up
                if gender == "M":    cat = "n-3f(1aS)"  # made up
                elif gender == "F":  cat = "n-1c"
                elif gender == "N":  cat = "n-3f(1aS)"
                else: assert False
            elif cat == "a-2b":
                if gender == "M":    cat = "n-3e(5bF)"  # made up
                elif gender == "F":  cat = "n-1a"
                elif gender == "N":  cat = "n-3e(5bF)"
                else: assert False
            elif cat == "a-3a":
                if gender == "M":    cat = "n-2a"
                elif gender == "F":  cat = "n-2b"
                elif gender == "N":  cat = "n-2c"
                else: assert False
            elif cat == "a-3b(1)":
                if gender == "M":    cat = "n-2a"
                elif gender == "F":  cat = "n=1a/2b"
                elif gender == "N":  cat = "n-2c"
                else: assert False
            elif cat == "a-3b(2)":
                if gender == "M":    cat = "n-2a"
                elif gender == "F":  cat = "n=1b/2b"
                elif gender == "N":  cat = "n-2c"
                else: assert False
            elif cat == "a-4a":
                if gender == "M":    cat = "n-3d(2aA)"  # made up
                elif gender == "F":  cat = "n-3d(2aA)"
                elif gender == "N":  cat = "n-3d(2bA)"  # made up
                else: assert False
            elif cat == "a-4b(1)":
                if gender == "M":    cat = "n-3f(1bA)"  # made up
                elif gender == "F":  cat = "n-3f(1bA)"
                elif gender == "N":  cat = "n-3f(1bA)"
                else: assert False
            elif cat == "a-4b(2)":
                if gender == "M":    cat = "n-3f(TIS)"  # made up
                elif gender == "F":  cat = "n-3f(TIS)"
                elif gender == "N":  cat = "n-3f(TIS)"
                else: assert False
            elif cat.startswith("v") or cat.startswith("cv"):
                if aspect_voice == "PA":
                    if gender == "M":    cat = "n-3c(5-PAP)"
                    elif gender == "F":  cat = "n-1c"
                    elif gender == "N":  cat = "n-3c(5-PAP)"
                    else: assert False
                elif aspect_voice == "PM":
                    if gender == "M":    cat = "n-2a"
                    elif gender == "F":  cat = "n-1b"
                    elif gender == "N":  cat = "n-2c"
                    else: assert False
                elif aspect_voice == "AA":
                    if gender == "M":    cat = "n-3c(5a-AAP)"
                    elif gender == "F":  cat = "n-1c"
                    elif gender == "N":  cat = "n-3c(5a-AAP)"
                    else: assert False
                elif aspect_voice == "AM":
                    if gender == "M":    cat = "n-2a"
                    elif gender == "F":  cat = "n-1b"
                    elif gender == "N":  cat = "n-2c"
                    else: assert False
                elif aspect_voice == "AP":
                    if gender == "M":    cat = "n-3c(5a-APP)"
                    elif gender == "F":  cat = "n-1c"
                    elif gender == "N":  cat = "n-3c(5a-APP)"
                    else: assert False
                elif aspect_voice == "XA":
                    if gender == "M":    cat = "n-3c(1-XAP)"
                    elif gender == "F":  cat = "n-1a(XAP)"
                    elif gender == "N":  cat = "n-3c(1-XAP)"
                    else: assert False
                elif aspect_voice == "XM":
                    if gender == "M":    cat = "n-2a"
                    elif gender == "F":  cat = "n-1b"
                    elif gender == "N":  cat = "n-2c"
                    else: assert False
                elif aspect_voice == "FA":
                    if gender == "M":    cat = "n-3c(5-PAP)"
                    elif gender == "F":  cat = "n-1c"
                    elif gender == "N":  cat = "n-3c(5-PAP)"
                    else: assert False
                elif aspect_voice == "FM":
                    if gender == "M":    cat = "n-2a"
                    elif gender == "F":  cat = "n-1b"
                    elif gender == "N":  cat = "n-2c"
                    else: assert False
                elif aspect_voice == "FP":
                    if gender == "M":    cat = "n-2a"
                    elif gender == "F":  cat = "n-1b"
                    elif gender == "N":  cat = "n-2c"
                    else: assert False
                else: assert False, aspect_voice
            new_mounce_cat.append(cat)

        orig_norm = norm
        norm = strip_accents(norm)
        norm = norm.replace("ἡ", "hη")
        norm = norm.replace("ὁ", "hο")
        norm = norm.replace("οὑ", "hου")
        norm = norm.replace("οἱ", "hοι")
        norm = norm.replace("αἱ", "hαι")
        norm = norm.replace("εἱ", "hει")
        norm = norm.replace("ἁ", "hα")
        norm = norm.replace("ἑ", "hε")
        norm = norm.replace("ὡ", "hω")
        norm = norm.replace("ὑ", "hυ")
        norm = norm.replace("ᾑ", "hῃ")
        norm = norm.replace("ᾡ", "hῳ")
        norm = norm.replace("οὐ", "ου")
        norm = norm.replace("ὠ", "ω")
        norm = norm.replace("ὀ" ,"ο")
        norm = norm.replace("ἀ", "α")

        success = False
        for ending_and_class_regex in noun_endings[case_number + gender]:
            l = len(ending_and_class_regex.split())
            if l == 3:
                ending, class_regex, explanation = ending_and_class_regex.split()
            elif l == 2:
                ending, class_regex = ending_and_class_regex.split()
                explanation = None
            else:
                ending = ending_and_class_regex
                class_regex = None
                explanation = None

            if norm.endswith(ending.replace(".", "")):
                success = True
                for cat in new_mounce_cat:
                    if not re.match(class_regex, cat):
                        success = False
                        break
                if success is True:
                    break

        if not success:
            print("@@@", row["bcv"], lemma, gender, case_number, mounce_cat, aspect_voice)
            print(norm, " / ".join(new_mounce_cat).replace("(", "\\(").replace(")", "\\)"))
            quit()

        if "." in ending:
            ending = ending[ending.find(".") + 1:]
        theme = orig_norm[:len(orig_norm) - len(ending)]
        if len(ending) == 0:
            orig_ending = ""
        else:
            orig_ending = orig_norm[-len(ending):]
        if aspect_voice == "--":
            assert orig_norm == theme + orig_ending, (orig_norm, theme, orig_ending)
            theme_by_lemma[lemma][gender].add(strip_accents(theme))
            forms_by_lemma[lemma][gender][case_number].add((orig_norm, theme, orig_ending, explanation))
        else:
            theme_by_lemma[lemma][aspect_voice + gender].add(strip_accents(theme))
            forms_by_lemma[lemma][aspect_voice + gender][case_number].add((orig_norm, theme, orig_ending, explanation))


collator = Collator()

for k in sorted(forms_by_lemma.keys(), key=collator.sort_key):
    print("{}:".format(k))
#    print("    gender: {}".format(", ".join(sorted(forms_by_lemma[k].keys(), key=lambda x: {"M": 0, "F": 1, "N": 2, "-": 3}[x]))))
    print("    mounce: {}".format(", ".join(sorted(mounce_by_lemma[k]))))
    print("    forms:")
    for gender in ["M", "F", "N", "-"]:
        if gender in forms_by_lemma[k]:
            print("        {}:".format(gender))
            print("            theme(s): {}".format(
                "/".join(theme_by_lemma[k][gender])
            ))
            for case_number in ["NS", "GS", "DS", "AS", "VS", "NP", "VP", "GP", "DP", "AP"]:
                if case_number in forms_by_lemma[k][gender]:
                    print("            {}: {}".format(case_number, " / ".join("{} {}|{} {}".format(n, t, e1, "" if not e2 else e2) for n, t, e1, e2 in forms_by_lemma[k][gender][case_number])))
    for aspect_voice in ["PA", "PM", "AA", "AM", "AP", "FA", "FM", "FP", "XA", "XM"]:
        printed_aspect_voice_yet = False
        for gender in ["M", "F", "N", "-"]:
            if aspect_voice + gender in forms_by_lemma[k]:
                if printed_aspect_voice_yet is False:
                    print("        {}:".format(aspect_voice))
                    printed_aspect_voice_yet = True
                print("            {}:".format(gender))
                print("                theme(s): {}".format(
                    "/".join(theme_by_lemma[k][aspect_voice + gender])
                ))
                for case_number in ["NS", "GS", "DS", "AS", "VS", "NP", "VP", "GP", "DP", "AP"]:
                    if case_number in forms_by_lemma[k][aspect_voice + gender]:
                        print("                {}: {}".format(
                            case_number,
                            " / ".join(
                                "{} {}|{} {}".format(
                                    n, t, e1, "" if not e2 else e2
                                ) for n, t, e1, e2 in forms_by_lemma[k][aspect_voice + gender][case_number])))
