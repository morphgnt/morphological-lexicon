#!/usr/bin/env python3

from morphgnt.utils import load_yaml, sorted_items

lexemes = load_yaml("lexemes.yaml")

# skip these for now until we work out how to handle them
SKIP = ["Ἀππίου", "Λιμήν", "Πάγος", "Πόλις", "Ταβέρνη", "Φόρον"]

for lexeme, metadata in sorted_items(lexemes):
    if "full-citation-form" in metadata and lexeme not in SKIP:
        lexeme = lexeme.split("/")[0]
        citation_form = metadata["full-citation-form"]
        print("{}: {}".format(lexeme, citation_form))
        for alt in citation_form.split(" / "):
            components = alt.split(", ")
            assert len(components) <= 6
            if len(components) == 1:
                assert components[0] == lexeme
            elif len(components) == 2:
                assert components[0] == lexeme
                assert components[1] in ["ὁ", "ἡ", "τό"]
            elif len(components) == 3:
                if components[2].startswith(("acc.", "dat.", "pl.")):
                    assert components[0] == lexeme
                    assert components[1] in ["ὁ", "ἡ", "τό", "τά"]
                else:
                    assert components[0] == lexeme
                    assert components[2] in [
                        "ὁ", "ἡ", "τό", "ὁ/ἡ", "ὁ/τό", "οἱ", "αἱ", "τά"]
                    if components[2] in ["οἱ", "αἱ", "τά"]:
                        assert components[1].endswith(("ων", "ῶν"))
            elif len(components) == 4:
                if components[3].startswith(
                        ("acc.", "dat.", "pl.", "contracted")
                ):
                    assert components[0] == lexeme
                    assert components[2] in ["ὁ", "ἡ", "τό"]
                else:
                    assert False
            elif len(components) == 6:
                if components[3].startswith("acc."):
                    assert components[0] == lexeme
                    assert components[2] in ["ὁ", "ἡ", "τό"]
                    assert components[4].startswith("dat.")
                    assert components[5].startswith("voc.")
