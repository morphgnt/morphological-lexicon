`abbott-smith.tei.xml` is from https://github.com/translatable-exegetical-tools/Abbott-Smith

`extract_headwords.py` extracts information from `abbott-smith.tei.xml` which
was then manually cleaned up to produce `abbott_smith_headwords.txt`.

`abbott_smith_headwords.txt` is a pipe-delimited file with three fields:
   * the lemma from the `entry` element's `n` attribute
   * the Strong's number from the `entry` element's `n` attribute
   * the text of the `form` element with all other markup stripped
