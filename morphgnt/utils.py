import unicodedata
import yaml

from pyuca import Collator
collator = Collator()


def load_yaml(filename, wrapper=lambda key, metadata: metadata):
    with open(filename) as f:
        return {
            key: wrapper(key, metadata)
            for key, metadata in (yaml.load(f) or {}).items()
        }


def load_wordset(filename):
    with open(filename) as f:
        return set(
            [word.split("#")[0].strip() for word in f if word.split("#")[0].strip()]
        )


def nfkc_normalize(s):
    return unicodedata.normalize("NFKC", s)


def sorted_items(d):
    return sorted(d.items(), key=lambda x: collator.sort_key(x[0]))


def stemmer(form, end_rule):
    if ">" in end_rule and "<" in end_rule:
        if "|" in end_rule[:end_rule.find(">")]:
            before1 = end_rule[:end_rule.find("|")]
            before2 = end_rule[end_rule.find("|") + 1:end_rule.find(">")]
        else:
            before1 = ""
            before2 = end_rule[:end_rule.find(">")]
        middle = end_rule[end_rule.find(">") + 1: end_rule.find("<")]
        if "|" in end_rule[end_rule.find("<") + 1:]:
            # after1 = end_rule[end_rule.find("<") + 1:end_rule.find("|", end_rule.find("<"))]
            after2 = end_rule[end_rule.find("|", end_rule.find("<")) + 1:]
        else:
            # after1 = end_rule[end_rule.find("<") + 1:]
            after2 = ""

        if not form.endswith(before1 + middle + after2):
            proposed_stem = None
        else:
            if len(middle + after2):
                proposed_stem = form[:-len(before1 + middle + after2)] + before1 + before2
            else:
                proposed_stem = form[:-len(before1 + middle + after2)] + before1 + before2
    else:
        if end_rule != "." and not form.endswith(end_rule):
            proposed_stem =  None
        else:
            if end_rule == ".":
                proposed_stem = form
            else:
                proposed_stem = form[:-len(end_rule)]

    return proposed_stem


if __name__ == "__main__":
    # A>B<C
    assert stemmer("XB", "A>B<C") == "XA"
    assert stemmer("B", "A>B<C") == "A"
    assert stemmer("C", "A>B<C") is None
    # A><
    assert stemmer("X", "A><") == "A"
    # A>B<C|D
    assert stemmer("XBD", "A>B<C|D") == "XA"
    assert stemmer("BD", "A>B<C|D") == "A"
    assert stemmer("BDE", "A>B<C|D") is None
    assert stemmer("BDE", "A>B<C|DE") == "A"
    assert stemmer("B", "A>B<C|D") is None
    assert stemmer("E", "A>B<C|D") is None
    # A|B><
    print(stemmer("A", "A|B><"), "AB")
    print(stemmer("XA", "A|B><"), "XAB")
    print(stemmer("AB", "A|B><"), None)
    print(stemmer("XAB", "A|B><"), None)
    # A|B>C<D|E

