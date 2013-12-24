#!/usr/bin/env python

import sys

from morphgnt import filesets
from morphgnt.utils import load_yaml, sorted_items

lexemes = load_yaml("lexemes.yaml")
forms = load_yaml("forms.yaml")
fs = filesets.load("filesets.yaml")

for row in fs["sblgnt-forms"].rows():
    lexeme = lexemes.get(row["lemma"].decode("utf-8"))
    if lexeme:
        lemma = row["lemma"].decode("utf-8")
        form = row["norm"].decode("utf-8")
        if lexeme["pos"] in ["RA", "A", "N", "RR"]:
            gender = row["ccat-parse"][6]
            case_number = row["ccat-parse"][4:6]
            form_list = forms.setdefault(lemma, {}).setdefault(gender, {}).setdefault(case_number, {}).setdefault("forms", [])
            if {"form": form} not in form_list:
                form_list.append({"form": form})
        elif lexeme["pos"] in ["RP1"]:
            case_number = row["ccat-parse"][4:6]
            form_list = forms.setdefault(lemma, {}).setdefault(case_number, {}).setdefault("forms", [])
            if {"form": form} not in form_list:
                form_list.append({"form": form})
        elif lexeme["pos"] in ["V"]:
            mood = row["ccat-parse"][3]
            if mood in ["N"]:
                tense_voice_mood = row["ccat-parse"][1:4]
                form_list = forms.setdefault(lemma, {}).setdefault(tense_voice_mood, {}).setdefault("forms", [])
                if {"form": form} not in form_list:
                    form_list.append({"form": form})
            elif mood in ["I", "D", "S", "O"]:
                tense_voice_mood = row["ccat-parse"][1:4]
                person_number = row["ccat-parse"][0] + row["ccat-parse"][5]
                form_list = forms.setdefault(lemma, {}).setdefault(tense_voice_mood, {}).setdefault(person_number, {}).setdefault("forms", [])
                if {"form": form} not in form_list:
                    form_list.append({"form": form})
            elif mood in ["P"]:
                tense_voice_mood = row["ccat-parse"][1:4]
                gender = row["ccat-parse"][6]
                case_number = row["ccat-parse"][4:6]
                form_list = forms.setdefault(lemma, {}).setdefault(tense_voice_mood, {}).setdefault(gender, {}).setdefault(case_number, {}).setdefault("forms", [])
                if {"form": form} not in form_list:
                    form_list.append({"form": form})
            else:
                print >>sys.stderr, "*** can't handle mood {}".format(mood)
        elif lexeme["pos"] in "P":
            form_list = forms.setdefault(lemma, {}).setdefault("forms", [])
            if {"form": form} not in form_list:
                form_list.append({"form": form})
    else:
        print >>sys.stderr, "lexemes file doesn't have {}".format(row["lemma"])


for form, metadata in sorted_items(forms):
    print "{}:".format(form.encode("utf-8"))
    pos = lexemes[form]["pos"]
    if pos in ["RA", "A", "N", "RR"]:
        for gender in ["M", "F", "N"]:
            if gender in metadata:
                print "    {}:".format(gender)
                for case_number in ["NS", "AS", "GS", "DS", "VS", "NP", "AP", "GP", "DP", "VP"]:
                    if case_number in metadata[gender]:
                        print "        {}:".format(case_number)
                        print "            forms:"
                        for form in metadata[gender][case_number]["forms"]:
                            print "                -"
                            print "                    form: {}".format(form["form"].encode("utf-8"))
    elif pos in ["RP1"]:
        for case_number in ["NS", "AS", "GS", "DS", "VS", "NP", "AP", "GP", "DP", "VP"]:
            if case_number in metadata:
                print "    {}:".format(case_number)
                print "        forms:"
                for form in metadata[case_number]["forms"]:
                    print "            -"
                    print "                form: {}".format(form["form"].encode("utf-8"))
    elif pos in ["V"]:
        for tense_voice_mood in [
            "AAN", "AMN", "APN",
            "FAN", "FMN",
            "PAN", "PMN", "PPN",
            "XAN", "XMN", "XPN",
        ]:
            if tense_voice_mood in metadata:
                print "    {}:".format(tense_voice_mood)
                print "        forms:"
                for form in metadata[tense_voice_mood]["forms"]:
                    print "            -"
                    print "                form: {}".format(form["form"].encode("utf-8"))
        for tense_voice_mood in [
            "AAI", "AAS", "AAD", "AAO",
            "AMI", "AMS", "AMD", "AMO",
            "API", "APS", "APD", "APO",
            "FAI",
            "FMI",
            "FPI",
            "IAI",
            "IMI",
            "IPI",
            "PAI", "PAS", "PAD", "PAO",
            "PMI", "PMS", "PMD", "PMO",
            "PPI", "PPS", "PPD",
            "XAI", "XAS", "XAD",
            "XMI",        "XMD",
            "XPI",
            "YAI",
            "YMI",
            "YPI",
        ]:
            if tense_voice_mood in metadata:
                print "    {}:".format(tense_voice_mood)
                for person_number in ["1S", "2S", "3S", "1P", "2P", "3P"]:
                    if person_number in metadata[tense_voice_mood]:
                        print "        {}:".format(person_number)
                        print "            forms:"
                        for form in metadata[tense_voice_mood][person_number]["forms"]:
                            print "                -"
                            print "                    form: {}".format(form["form"].encode("utf-8"))
        for tense_voice_mood in [
            "AAP", "AMP", "APP",
            "FAP", "FMP", "FPP",
            "PAP", "PMP", "PPP",
            "XAP", "XMP", "XPP",
        ]:
            if tense_voice_mood in metadata:
                print "    {}:".format(tense_voice_mood)
                for gender in ["M", "F", "N"]:
                    if gender in metadata[tense_voice_mood]:
                        print "        {}:".format(gender)
                        for case_number in ["NS", "AS", "GS", "DS", "VS", "NP", "AP", "GP", "DP", "VP"]:
                            if case_number in metadata[tense_voice_mood][gender]:
                                print "            {}:".format(case_number)
                                print "                forms:"
                                for form in metadata[tense_voice_mood][gender][case_number]["forms"]:
                                    print "                    -"
                                    print "                        form: {}".format(form["form"].encode("utf-8"))

    elif pos in "P":
        print "    forms:"
        for form in metadata["forms"]:
            print "        -"
            print "            form: {}".format(form["form"].encode("utf-8"))
    else:
        print >>sys.stderr, "*** can't handle pos {}".format(pos)


