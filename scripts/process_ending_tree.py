#!/usr/bin/env python3

from collections import defaultdict
from unicodedata import normalize

# (ending, parse)->int(count)
counts = defaultdict(int)

# (ending)->set(parse)
parses = defaultdict(set)

# (ending)->set(rule)
rules = defaultdict(set)


with open("ending_tree.txt") as stream:
    for line in stream:
        path, rule, parse, count = line.strip().split()
        for step in path.split("/"):
            counts[(step, parse)] += int(count)
            parses[step].add(parse)
            rules[step].add(int(rule.strip("{}")))


def collation_key(step):
    path = []
    if step.endswith("(ν)"):
        start = 3
    else:
        start = 1
    for j in range(start, min(6, len(step) + 1)):
        path.append(normalize("NFD", step[-j:]))
    return tuple(path)

for ending in sorted(parses, key=collation_key):
    if parses[ending] != parses[ending[1:]] or len(parses[ending]) > 1:
        print(
            "    " * (len(collation_key(ending)) - 1) + "-" + ending + ":",
            ";".join([
                "{}/{}".format(parse, counts[ending, parse])
                for parse in parses[ending]
            ]),
            rules[ending],
        )
