import yaml
import numpy
import pandas as pd
import numpy as np
from pprint import pprint
import sys
from PyOrgMode import PyOrgMode
import os

frags = []

elements = PyOrgMode.OrgDataStructure()
elements.load_from_file('elements.org')

all_els = []

def extract(root):
    base = [root.heading] if root.heading.strip() else []

    if all([type(node) is str for node in root.content]):
        all_els.append(root.heading)
    else:
        for node in root.content:
            if type(node) == str:
                continue

            extract(node)

extract(elements.root)

for study_path in sys.argv[1:]:
    pages = yaml.load(open(study_path))['pages']
    study = study_path[10:-4]

    for fragments in [p['fragments'] for p in pages.values()]:
        for fragment in fragments:
            coords = str(fragment.get('coords'))
            for element in fragment['elements']:
                frags.append(dict(Study=study,
                                  Fragment=coords,
                                  Element=element))

df = pd.DataFrame(frags)

out = df.groupby(['Study', 'Element'])['Fragment'] \
        .count() \
        .unstack() \
        .fillna(0) \
        .applymap(np.int) \
        .to_latex()

for element in all_els:
    out = out.replace(element, '\\rot{%s}' % element, 1)

print(out)
