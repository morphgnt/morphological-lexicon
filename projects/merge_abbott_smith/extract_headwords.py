#!/usr/bin/env python3

import xml.etree.ElementTree as ET

tree = ET.parse("abbott-smith.tei.xml")

ns = {
    "TEIOSIS": "http://www.crosswire.org/2013/TEIOSIS/namespace"
}

body = tree.getroot().find("TEIOSIS:text/TEIOSIS:body", ns)

for entry in body.findall(".//TEIOSIS:entry", ns):
    entry_n = entry.get("n")
    form = entry.find("TEIOSIS:form", ns)
    assert form.attrib == {}
    if form.text:
        s = form.text
    else:
        s = ""
    for child in form.itertext():
        s += child
    assert "|" not in s
    print(entry_n + "|" + s)
