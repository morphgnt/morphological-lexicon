#!/usr/bin/env python3

from pysblgnt import morphgnt_rows
from pyuca import Collator
import yaml

from characters import strip_accents
from morphgnt.utils import load_wordset

from collections import defaultdict
import re

IGNORE_SET = load_wordset("../../nominal-indeclinable.txt")

IGNORE_SET.update({
    "ὅδε",
    "τοιόσδε",
    "ὅστις",
})

LEMMA_OVERRIDE = {
    "μήν": "μήν/N",
}

MOUNCE_OVERRIDES = {
    "ἄγαμος": "n=2a/2b",
    "αἴτιον": "a-1a(1)",  # should it be αἴτιος?
    # "ἀκριβέστερον",
    "ἄκων": "a-2a(2)",
    "ἅλα": "n-3c(6aALA)",  # @@@
    "ἀλάβαστρος": "n-2b",
    "ἄλλος": "a=1a(2b-HOS)",
    "ἀλλήλων": "a=1a(2b-HOS)",  # @@@
    # "ἀλυπότερος",
    "ἀμφιέννυμι": "v-3c(1)",
    # "ἀνάθεμα",  # @@@ lemmatization bug?
    # "ἀνώτερος",
    "ἄπειμι": "cv-6b",
    "αὐτός": "a=1a(2b-HOS)",
    "ἄψινθος": "n-2b",
    "βάθος": "n-3d(2b)",
    "βασίλειον": "a-3a",  # should it be βασίλειος in Luke?
    "βάτος": "n=2a/2b",
    # "βέλτιον",
    "γυνή": "n=3b(1GUNH)",
    "δάκρυον": "n=2c(SIN)",  # n-2c with σι(ν) DPN
    "δεῖνα": "n-3f(1a)",
    "δεκάτη": "a-1a(2a)",  # should it be δέκατος
    "δεσμόν": "n-2c",
    "διάκονος": "n=2a/2b",
    "διαπλέω": "cv-1a(7)",
    "δοῦλος": "a-1a(2a)",  # @@@
    "δύο": "a-5(DUO)",
    "δύσις": "n-3e(5b)",
    "ἑαυτοῦ": "a=1a(2b-HOS)",  # @@@
    "εἰδωλόθυτον": "a-3a",  # should it be εἰδωλόθυτος ?
    "εἷς": "a=4b(2-EIS)",
    "εἴωθα": "v-1b(3)",
    "ἑκατοντάρχης": "n=1f/n-2a",  # lemmatization issue?
    "ἐκεῖνος": "a=1a(2b-HOS)",
    "ἑκών": "a-2a(2)",  # made up subcategory to select n-3c(5b) in masculine/neuter
    "ἔννυχα": "a-3a",  # incorrect lemma?
    "ἐξανάστασις": "n-3e(5b)",
    "ἐξανάστασις": "n-3e(5b)",
    "ἔρημος": "a-3a",
    "ἔρις": "n=3c(2-ERIS)",
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
    "κἀκεῖνος": "a=1a(2b-HOS)",
    "κακοποιός": "a-3a",
    "κάμηλος": "n-2b",
    "κλείς": "n=3c(2KLEIS)",
    "λεπτόν": "a-1a(2a)",  # @@@ lemma?
    "λιμός": "n=2a/2b",
    "Μαθθαῖος": "n-2a",
    "Μαθθίας": "n-1d",
    "μάταιος": "a=1a(1)/a-3",
    "μέγας": "a=1a(2a-MEGAS)",
    "μέλαν": "a-2a(3)",  # made up subcategory
    "μηδείς": "a=4b(2-EIS)",
    "μήν": "n-3f(1a)",
    "μητρολῴας": "n-1d",
    "μίγνυμι": "v-3c(2)",
    "νηφάλιος": "a-3a",  # @@@
    "νουμηνία": "n-1a",
    "νύμφη": "n-1b",
    "ὁ": "a=1a(2b-HO)",
    "ὅς": "a=1a(2b-HOS)",
    "οἶμαι": "v-1d(2c)",
    "ὄνος": "n=2a/2b",  # masculine in Luke
    "ὅσιος": "a-3a",  # @@@
    "ὀστέον": "n-2d",
    "οὐδείς": "a=4b(2-EIS)",
    "οὖς": "n=3c(6c-OUS)",
    "οὗτος": "a=1a(2b-HOS)",
    "ὀψία": "n-1a",
    "παραπλήσιον": "a-1a(1)",
    "παρθένος": "n=2a/2b",  # only masculine in Revelation
    "παρίστημι": "cv-6a",
    "Πέργαμος": "n-2b",
    "πλοῦτος": "n=2a(PLOUTOS)",
    "πολύς": "a=1a(2a-POLUS)",
    "πυκνά": "a-1a(2a)",  # change to πυκνός in Luke?
    "σάββατον": "n=2c(SAB)",  # n-2c with σι(ν) DPN
    "σεαυτοῦ": "a=1a(2b-HOS)",  # @@@
    "σκῦλα": "n-2c",  # change to σκῦλον?
    "στάδιος": "n-2a",
    "στάμνος": "n-2b",
    "στάχυς": "n-3e(1)",
    "συνομιλέω": "cv-1d(2a)",
    # "τάχιον",
    "ταχύ": "adverb",
    "τέσσαρες": "a-4c",
    "τηλικοῦτος": "a=1a(2b-HOS)",
    "τιμιότης": "n-3c(1)",
    "τίς": "a-4b(2-TIS)",
    "τις": "a-4b(2-TIS)",
    # "τομώτερος",
    "τοιοῦτος": "a=1a(2b-HOS)",
    "τοσοῦτος": "a=1a(2b-HOSb)",
    "τοὔνομα": "n-3c(4)",
    "τρεῖς": "a=4a(TREIS)",
    "τριετία": "n-1a",
    "τρίμηνον": "a-3a",  # should it be τρίμηνος?
    "ὕαλος": "n-2a",
    # "ὕστερον",
    "φοβέομαι": "v-1d(2a)",  # ?
    "χείμαρρος": "n-2a",
    "χείρ": "n=3f(2a-XEIR)",
    "χρύσεος": "a-1b",  # should it be χρύσους?
    "ψίξ": "n-3b(3)",
}

forms_by_lemma = defaultdict(lambda: defaultdict(lambda: defaultdict(set)))
mounce_by_lemma = defaultdict(set)
theme_by_lemma = defaultdict(lambda: defaultdict(set))

stems_and_class_by_lemma = defaultdict(lambda: defaultdict(lambda: defaultdict(set)))

with open("nominal_endings.yaml") as f:
    noun_endings = yaml.load(f)

with open("../../lexemes.yaml") as f:
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

        if lemma in IGNORE_SET:
            continue

        if lemma[0].lower() != lemma[0]:
            continue

        if lemma in LEMMA_OVERRIDE:
            lemma = LEMMA_OVERRIDE[lemma]
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
                cat = {
                    "M": "n-2a",
                    "F": "n-1a",
                    "N": "n-2c",
                }[gender]
            elif cat == "a=1a(1)/a-3":
                cat = {
                    "M": "n-2a",
                    "F": "n=1a/2b",
                    "N": "n-2c",
                }[gender]
            elif cat == "a-1a(2a)":
                cat = {
                    "M": "n-2a",
                    "F": "n-1b",
                    "N": "n-2c",
                }[gender]
            elif cat == "a=1a(2a-POLUS)":
                cat = {
                    "M": "n=2a(POLUS)",
                    "F": "n-1b",
                    "N": "n=2c(POLUS)",
                }[gender]
            elif cat == "a=1a(2a-MEGAS)":
                cat = {
                    "M": "n=2a(MEGAS)",
                    "F": "n-1b",
                    "N": "n=2c(MEGAS)",
                }[gender]
            elif cat == "a=1a(2b-HO)":
                cat = {
                    "M": "n=2a(HO)",
                    "F": "n=1b(HO)",
                    "N": "n=2c(HO)",
                }[gender]
            elif cat == "a=1a(2b-HOS)":
                cat = {
                    "M": "n=2a(HOS)",  # can get rid of? @@@
                    "F": "n=1b(HOS)",  # can get rid of? @@@
                    "N": "n=2c(HOS)",
                }[gender]
            elif cat == "a=1a(2b-HOSb)":
                cat = {
                    "M": "n-2a",
                    "F": "n-1b",
                    "N": "n=2c(HOSb)",
                }[gender]
            elif cat == "a-1b":
                cat = {
                    "M": "n-2d",
                    "F": "n-1h",
                    "N": "n-2d",
                }[gender]
            elif cat == "a-2a":
                cat = {
                    "M": "n-3c(5a)",
                    "F": "n-1c",
                    "N": "n-3c(5a)",
                }[gender]
            elif cat == "a-2a(2)":  # made up
                cat = {
                    "M": "n-3c(5b)",
                    "F": "n-1c",
                    "N": "n-3c(5b)",
                }[gender]
            elif cat == "a-2a(3)":  # made up
                cat = {
                    "M": "n-3f(1aS)",  # made up
                    "F": "n-1c",
                    "N": "n-3f(1aS)",
                }[gender]
            elif cat == "a-2b":
                cat = {
                    "M": "n-3e(5bF)",  # made up
                    "F": "n-1a",
                    "N": "n-3e(5bF)",
                }[gender]
            elif cat == "a-3a":
                cat = {
                    "M": "n-2a",
                    "F": "n-2b",
                    "N": "n-2c",
                }[gender]
            elif cat == "a-3b(1)":
                cat = {
                    "M": "n-2a",
                    "F": "n=1a/2b",
                    "N": "n-2c",
                }[gender]
            elif cat == "a-3b(2)":
                cat = {
                    "M": "n-2a",
                    "F": "n=1b/2b",
                    "N": "n-2c",
                }[gender]
            elif cat == "a-4a":
                cat = {
                    "M": "n-3d(2aA)",  # made up
                    "F": "n-3d(2aA)",
                    "N": "n-3d(2bA)",  # made up
                }[gender]
            elif cat == "a=4a(TREIS)":
                cat = {
                    "M": "n-3d(2aA-TREIS)",  # made up
                    "F": "n-3d(2aA-TREIS)",
                    "N": "n-3d(2bA-TREIS)",  # made up
                }[gender]
            elif cat == "a-4b(1)":
                cat = {
                    "M": "n-3f(1bA)",  # made up
                    "F": "n-3f(1bA)",
                    "N": "n-3f(1bA)",
                }[gender]
            elif cat == "a-4b(2-TIS)":
                cat = {
                    "M": "n-3f(TIS)",  # made up
                    "F": "n-3f(TIS)",
                    "N": "n-3f(TIS)",
                }[gender]
            elif cat == "a=4b(2-EIS)":
                cat = {
                    "M": "n-3f(EIS)",  # made up
                    "F": "n=1a(EIS)",
                    "N": "n-3f(EIS)",
                }[gender]
            elif cat.startswith("v") or cat.startswith("cv"):
                if aspect_voice == "PA":
                    cat = {
                        "M": "n-3c(5-PAP)",  # made up
                        "F": "n-1c",
                        "N": "n-3c(5-PAP)",
                    }[gender]
                elif aspect_voice == "PM":
                    cat = {
                        "M": "n-2a",
                        "F": "n-1b",
                        "N": "n-2c",
                    }[gender]
                elif aspect_voice == "AA":
                    cat = {
                        "M": "n-3c(5a-AAP)",  # made up
                        "F": "n-1c",
                        "N": "n-3c(5a-AAP)",
                    }[gender]
                elif aspect_voice == "AM":
                    cat = {
                        "M": "n-2a",
                        "F": "n-1b",
                        "N": "n-2c",
                    }[gender]
                elif aspect_voice == "AP":
                    cat = {
                        "M": "n-3c(5a-APP)",  # made up
                        "F": "n-1c",
                        "N": "n-3c(5a-APP)",
                    }[gender]
                elif aspect_voice == "XA":
                    cat = {
                        "M": "n-3c(1-XAP)",  # made up
                        "F": "n-1c",
                        "N": "n-3c(1-XAP)",
                    }[gender]
                elif aspect_voice == "XM":
                    cat = {
                        "M": "n-2a",
                        "F": "n-1b",
                        "N": "n-2c",
                    }[gender]
                elif aspect_voice == "FA":
                    cat = {
                        "M": "n-3c(5-PAP)",
                        "F": "n-1c",
                        "N": "n-3c(5-PAP)",
                    }[gender]
                elif aspect_voice == "FM":
                    cat = {
                        "M": "n-2a",
                        "F": "n-1b",
                        "N": "n-2c",
                    }[gender]
                elif aspect_voice == "FP":
                    cat = {
                        "M": "n-2a",
                        "F": "n-1b",
                        "N": "n-2c",
                    }[gender]
                else:
                    assert False, aspect_voice

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
        norm = norm.replace("ὀ", "ο")
        norm = norm.replace("ἀ", "α")

        success = False
        for ending_and_class_regex in noun_endings[case_number + gender]:
            try:
                ending, class_regex, explanation = ending_and_class_regex.split()
            except ValueError:
                print("{}\n{} {}".format(row["bcv"], case_number + gender, ending_and_class_regex))
                quit()

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
    print("    mounce: {}".format(", ".join(sorted(mounce_by_lemma[k]))))
    print("    forms:")
    for gender in ["M", "F", "N", "-"]:
        if gender in forms_by_lemma[k]:
            print("        {}:".format(gender))
            print("            theme(s): {}".format(
                "/".join(sorted(theme_by_lemma[k][gender]))
            ))
            for case_number in ["NS", "GS", "DS", "AS", "VS", "NP", "VP", "GP", "DP", "AP"]:
                if case_number in forms_by_lemma[k][gender]:
                    print("            {}: {}".format(case_number, " / ".join("{} {}|{} {}".format(n, t, e1, "" if not e2 else e2) for n, t, e1, e2 in sorted(forms_by_lemma[k][gender][case_number]))))
    for aspect_voice in ["PA", "PM", "AA", "AM", "AP", "FA", "FM", "FP", "XA", "XM"]:
        printed_aspect_voice_yet = False
        for gender in ["M", "F", "N", "-"]:
            if aspect_voice + gender in forms_by_lemma[k]:
                if printed_aspect_voice_yet is False:
                    print("        {}:".format(aspect_voice))
                    printed_aspect_voice_yet = True
                print("            {}:".format(gender))
                print("                theme(s): {}".format(
                    "/".join(sorted(theme_by_lemma[k][aspect_voice + gender]))
                ))
                for case_number in ["NS", "GS", "DS", "AS", "VS", "NP", "VP", "GP", "DP", "AP"]:
                    if case_number in forms_by_lemma[k][aspect_voice + gender]:
                        print("                {}: {}".format(
                            case_number,
                            " / ".join(
                                "{} {}|{} {}".format(
                                    n, t, e1, "" if not e2 else e2
                                ) for n, t, e1, e2 in sorted(forms_by_lemma[k][aspect_voice + gender][case_number]))))
