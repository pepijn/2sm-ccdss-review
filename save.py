import sys
from sys import exit
from PyOrgMode import PyOrgMode
from pprint import pprint
import popplerqt4
import sys
import PyQt4
import textwrap
from pprint import pprint
import yaml
import re

org = PyOrgMode.OrgDataStructure()
org.load_from_string(sys.stdin.read())

pages = {}

for node in org.root.content:
    annotation = dict(elements={})

    properties = node.content[0].content

    coords = []
    for coord in properties[1:]:
        assert coord.name == 'COORDS'
        coords.append(coord.value)

    coords = [[int(s) for s in str.split(coord, ',')] for coord in coords]

    annotation.update(coords=list(coords))

    for line in node.content[1:]:
        match = re.match('\s+- \[X\] (.+)', line)
        if not match:
            continue
        element = match.groups()[0]
        # Force 'block style'
        # http://pyyaml.org/wiki/PyYAMLDocumentation#Dictionarieswithoutnestedcollectionsarenotdumpedcorrectly
        annotation['elements'][element] = []

    if not annotation['elements']:
        continue

    page_number = int(properties[0].value)
    page = pages.get(page_number, None)
    if not page:
        page = pages[page_number] = []

    page.append(annotation)

print(yaml.dump(dict(pages={k: dict(fragments=v) for k,v in pages.items()})))
