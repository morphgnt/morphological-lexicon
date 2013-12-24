import os.path

from .utils import load_yaml


class FileSet(object):

    def __init__(self, setname, metadata):
        self.setname = setname
        self.metadata = metadata

    def files(self):
        for filename in self.metadata["files"]:
            yield os.path.abspath(os.path.join(self.metadata["prefix"], filename))

    def rows(self):
        for filename in self.files():
            with open(filename) as f:
                for line in f:
                    yield dict(zip(
                        ("bcv", "ccat-pos", "ccat-parse", "robinson", "text", "word", "norm", "lemma"),
                        line.strip().split()
                    ))


def load(filename):
    return load_yaml(filename, FileSet)
