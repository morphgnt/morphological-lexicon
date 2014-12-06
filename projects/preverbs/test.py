#!/usr/bin/env python3

with open("prepositions.txt") as f:
    PREPOSITIONS = [line.strip() for line in f.readlines()]


with open("verbs.txt") as f:
    for line in f:
        if line.startswith("#"):
            continue
        if line.strip() == "":
            continue
        content_comment = line.split("#")
        content = content_comment[0].strip()
        if len(content_comment) == 2:
            comment = content_comment[1].strip()
        else:
            comment = None

        if comment:
            assert set(comment.split()) < {"note.1", "note.2", "note.3", "note.4", "@@@"}, comment

        lemma_analysis = content.split("|")

        if len(lemma_analysis) != 2:
            raise Exception(content)

        lemma, analyses = content.split("|")
        if analyses == "@@@":
            continue

        for analysis in analyses.split(";"):
            components = analysis.split("+")
            if len(components) == 2:
                assert components[0] in PREPOSITIONS, analysis
            elif len(components) == 3:
                assert components[0] in PREPOSITIONS, analysis
                assert components[1] in PREPOSITIONS, analysis
            else:
                raise Exception(analysis)
