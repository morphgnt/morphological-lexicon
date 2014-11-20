## ending-paradigms.txt

Lines of the form

    <tense-voice>: <1S>, <2S>, <3S>, <1P>, <2P>, <3P>

e.g.

    PA: ω, εις, ει, ομεν, ετε, ουσι(ν)


## check_endings.py

Loads `ending-paradigms.txt` then reads MorphGNT, groups the indicative verb
forms by lemma and tense-voice then checks there's a line in
`ending-paradigms.txt` that matches.

@@@


## retired/paradigm.py

Was used to produced an earlier version of `ending-paradigms.txt`.


## princpal_parts.py

Produces `principal_parts.txt`. Looks otherwise very similar to
`check_endings.py` except that it outputs the full forms per lemma.

@@@
