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

elements = {}

def extract(root):
    branches = [extract(node) for node in root.content if hasattr(node, 'heading')]

    if any([node.heading[:8] == 'Fragment' for node in branches]):
        lines = [l for l in root.content if type(l) is str and l.strip()]

        if lines:
            elements[root.heading] = lines

    return root

extract(org.root)
print(yaml.dump(dict(elements=elements), default_flow_style=False))
