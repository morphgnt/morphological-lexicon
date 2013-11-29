# Morphological Lexicon of the Greek New Testament

analysis and explanation of morphology of Greek New Testament and similar texts

Only covers a fraction of text at the moment. Each cycle of work adds more
text, merges in more existing analysis and improves the code.

## Current Process

* add a file to 'sblgnt-lexemes` set in `filesets.yaml` (I'm doing shortest first)
* `./scripts/generate_lexemes.py >> lexemes.yaml`
* manual inspect `pos` and clean up morphgnt/tisch conflicts
* run `add_bdag_headwords.py`
* manually check all missing BDAG headwords
* run `add_dodson.py`
* clean up 0-padded numbers
* manually check all missing dodson entries
* run `add_mounce_morphcat.py`
* manually check all missing morphcat entries
* run `check_pos.py` and review pos inconsistencies
