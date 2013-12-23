import unicodedata
import yaml


def load_yaml(filename, wrapper=lambda key, metadata: metadata):
    with open(filename) as f:
        return {
            key: wrapper(key, metadata)
            for key, metadata in (yaml.load(f) or {}).items()
        }


def load_wordset(filename):
    with open(filename) as f:
        return set(
            [word.split("#")[0].strip().decode("utf-8") for word in f if word.split("#")[0].strip()]
        )


def nfkc_normalize(s):
    return unicodedata.normalize("NFKC", s)
