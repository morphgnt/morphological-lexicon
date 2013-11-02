from morphgnt import filesets


fs = filesets.load("filesets.yaml")

for row in fs["sblgnt-test"].rows():
    print row
