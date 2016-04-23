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
    [extract(node) for node in root.content if hasattr(node, 'heading')]

    if hasattr(root, 'todo'):
        lines = [l for l in root.content if type(l) is str and l.strip()]

        element = elements.setdefault(root.heading, {})

        for line in root.content:
            if type(line) is not str or line[0:2] == '#+':
                break

            match = re.match('- \[([X ])\] (.+)', line)
            if match:
                if match.groups()[0] == 'X':
                    clsn = element.setdefault('classification', [])
                    clsn.append(match.groups()[1])
            else:
                if line.strip():
                    element.setdefault('summary', "")
                    element['summary'] = element['summary'] + line + ' '
        if element.get('summary'):
            element['summary'] = element['summary'].strip()

    return root

extract(org.root)
print(yaml.dump(dict(elements=elements), default_flow_style=False))
