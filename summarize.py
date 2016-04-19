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

def extract(root):
    if type(root) is str:
        if root.strip():
            return root
        else:
            return

    for node in root.content:
        val = extract(node)
        if type(val) is str:
            element = root.heading

            if not elements.get(element, None):
                elements[element] = dict(MYCIN=[])

            elements[element]['MYCIN'].append(val)

extract(example.root)

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

struct = PyOrgMode.OrgDataStructure()
extraction = PyOrgMode.OrgNode.Element()
extraction.heading = 'Data extraction'
struct.root.append_clean('#+TITLE: Bachelor thesis progress summary\n')
struct.root.append_clean(extraction)

def extract(root):
    if type(root) is str:
        return root

    string_branches = [type(extract(node)) is str for node in list(root.content)]

    if all(string_branches):
        element = str(root.heading)
        root.content = []
        dones = 0
        not_dones = 0
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
                el.append_clean('- ' + line)
                el.append_clean('\n')
            el.append_clean('\n')

            root.append_clean(el)

        root.heading = element + " [%s/%s]" % (dones, dones + not_dones)
        root.append_clean('#+LaTeX: \\newpage\n')

    return root

extraction.append_clean(extract(example.root).content)

data = open('sources/excluded.csv')

exclusion_reasons = {}

for row in csv.DictReader(data):
    study = row.pop('Study')
    exclusion_reason = str.split(row.pop('Notes')[18:-1], ';')[0]
    if not exclusion_reasons.get(exclusion_reason, None):
        exclusion_reasons[exclusion_reason] = []
    exclusion_reasons[exclusion_reason].append(dict(
        study=study,
        title=row.pop('Title')
    ))

ex = PyOrgMode.OrgNode.Element()
ex.heading = 'Excluded'
struct.root.append_clean(ex)

ftr = PyOrgMode.OrgNode.Element()
ftr.heading = 'Full-text review'
ex.append_clean(ftr)

for exclusion_reason, studies in exclusion_reasons.items():
    reason = PyOrgMode.OrgNode.Element()
    reason.heading = exclusion_reason

    for study in studies:
        stdy = PyOrgMode.OrgNode.Element()
        stdy.heading = study['study']
        stdy.append_clean(study['title'])
        stdy.append_clean('\n')
        stdy.append_clean('\n')
        reason.append_clean(stdy)

    reason.append_clean('#+LaTeX: \\newpage\n')
    ftr.append_clean(reason)

struct.save_to_file('progress.org')
