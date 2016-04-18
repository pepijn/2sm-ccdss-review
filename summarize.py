import sys
from sys import exit
import poppler
import urllib
import os
from pdb import set_trace
import string
import csv
import re
from PyOrgMode import PyOrgMode
import textwrap
import dateutil.parser
from datetime import timedelta, datetime
from pprint import pprint

example = PyOrgMode.OrgDataStructure()
example.load_from_file('mycin.org')

elements = {}

studies = ['MYCIN']

data = open('sources/articles.csv')

for row in csv.DictReader(data):
    study = row.pop('Study')
    studies.append(study)

for category in example.root.content:
    for item in category.content:
        element = elements[item.heading] = {}
        contents = element[studies[0]] = []

        for line in item.content:
            if type(line) is not str:
                continue

            line = line.strip()

            if not line:
                continue

            contents.append(line)

files = sys.argv[1:]

for path in files:
    study = path[8:-4]
    base = PyOrgMode.OrgDataStructure()
    base.load_from_file(path)

    def extract(root):
        if type(root) is str:
            return

        # Is done
        if hasattr(root, 'scheduled'):
            element = None
            if root.parent.heading in elements.keys():
                element = root.parent.heading
            elif root.parent.parent.heading in elements.keys():
                element = root.parent.parent.heading

            if element:
                example = False
                for line in root.parent.content:
                    if type(line) is not str:
                        continue

                    line = line.strip()

                    if not line:
                        continue

                    if line == '#+END_EXAMPLE':
                        example = False
                        continue

                    if example:
                        continue

                    if line == '#+BEGIN_EXAMPLE':
                        example = True
                        continue

                    if not elements[element].get(study, None):
                        elements[element][study] = []

                    elements[element][study].append(line)

        for node in root.content:
            extract(node)

    extract(base.root)

for category in example.root.content:
    for item in category.content:
        dones = 0
        not_dones = 0
        element = item.heading
        item.content = []

        for study in studies:
            el = PyOrgMode.OrgNode.Element()
            el.heading = study

            lines = elements[element].get(study, [])
            if study == 'MYCIN':
                pass
            elif lines:
                dones += 1
                el.todo = 'DONE'
            else:
                not_dones += 1
                el.todo = 'TODO'

            for line in lines:
                el.append_clean(line)
                el.append_clean('\n')
            el.append_clean('\n')

            item.append_clean(el)

        item.heading = item.heading + " [%s/%s]" % (dones, dones + not_dones)
        item.append_clean('#+LaTeX: \\newpage\n')

example.root.content.insert(0, '#+LaTeX: \\newpage\n')
example.save_to_file('sources.org')
