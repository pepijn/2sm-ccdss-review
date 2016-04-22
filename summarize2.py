from sys import exit
from PyOrgMode import PyOrgMode
from pprint import pprint
import popplerqt4
import sys
import PyQt4
import textwrap
import yaml
import re

checklist = PyOrgMode.OrgDataStructure()
checklist.load_from_file('elements.org')
checklist.root.content.insert(0, '#+STARTUP: showall\n')

source = PyOrgMode.OrgDataStructure()
source.load_from_string(sys.stdin.read())

current = {}
for element_name, contents in (yaml.load(open(sys.argv[1])) or {}).get('elements', {}).items():
    current[element_name] = contents

elements = {}
el_indexes = []

classifications = ['Reported',
                   'Not reported',
                   'Inferred but nearly certain',
                   'Inferred and uncertain']

for fragment in source.root.content[1:]:
    for line in fragment.content[1:]:
        match = re.match('\s+- \[X\] (.+)', line)
        if not match:
            continue

        element = elements.setdefault(match.groups()[0], set())
        element.add(fragment)
        el_indexes.append(fragment)

def extract(root):
    if type(root) is str:
        return root

    branches = [type(extract(node)) is str for node in root.content]

    if all(branches):
        element = root.heading
        current_elements = elements.get(element, [])

        if current.get(element, {}).get('classification', []):
            root.todo = 'DONE'
        else:
            root.todo = 'TODO'

        root.content = []
        for classification in classifications:
            if classification in current.get(element, {}).get('classification', []):
                root.append_clean('- [X] %s\n' % classification)
            else:
                root.append_clean('- [ ] %s\n' % classification)

        root.append_clean('\n')

        for line in current.get(element, {}).get('summary', []):
            root.append_clean(line + '\n')
        root.append_clean('\n')

        for fragment in current_elements:
            el = PyOrgMode.OrgNode.Element()
            el.heading = "Fragment %s" % str(el_indexes.index(fragment) + 1)

            for line in fragment.content[:-2]:
                if type(line) is str and line[:8] == '- Common':
                    break

                el.append_clean(line)
                el.append_clean('\n')
            root.append_clean(el)

        root.append_clean('#+LaTeX: \\newpage\n')
    else:
        root.heading = root.heading + ' [%]'
        props = PyOrgMode.OrgDrawer.Element("PROPERTIES")
        props.append(PyOrgMode.OrgDrawer.Property("COOKIE_DATA", 'todo recursive'))
        root.content.insert(0, props)

    return root

checklist.root.content = [extract(n) for n in checklist.root.content]

import tempfile
with tempfile.NamedTemporaryFile() as t:
    checklist.save_to_file(t.name)
    print(t.read())
