import yaml
import numpy
import pandas as pd
import numpy as np
from pprint import pprint
import sys
from PyOrgMode import PyOrgMode
import os

script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in

def categories(path):
    elements = PyOrgMode.OrgDataStructure()
    elements.load_from_file(path)

    def extract(root):
        base = [root.heading] if root.heading.strip() else []

        if all([type(node) is str for node in root.content]):
            return base
        else:
            branches = [extract(node) for node in root.content if type(node) != str]
            results = []

            for branch in branches:
                for subbranch in branch:
                    if type(subbranch) is str:
                        results.append(base + [subbranch])
                    else:
                        results.append(base + subbranch)
            return results

    def tableize(items):
        result = dict(Element=items.pop(len(items) - 1))
        stadia = ['Category', 'Subcategory']
        for stadium in stadia:
            try:
                result[stadium] = items.pop(0)
            except IndexError:
                result[stadium] = ' '
        return result

    return [tableize(element) for element in extract(elements.root)]

filename = 'elements.org'

categories = categories(os.path.join(script_dir, filename))
orders = []
for item in categories:
    orders.append(item['Element'])
categories = pd.DataFrame(categories).set_index('Element')
rows = []

for study_path in sys.argv[1:]:
    elements = yaml.load(open(study_path))['elements']

    study_name = study_path[9:-4]

    for element, data in elements.items():
        data.update(dict(Study=study_name,
                         Element=element,
                         Summary=data.pop('summary', None)))

        rows.append(data)

df = pd.DataFrame(rows) \
       .join(categories, on='Element') \
       .set_index(['Study', 'Category', 'Subcategory', 'Element'])

def classify(flags):
    classifications = {
        ('Reported', 'Not reported'): ['Partially reported']
    }

    return classifications.get(tuple(flags), flags)[0]

classifications = df['classification']
df['flags'] = classifications.map(lambda cs: ', '.join(cs))
df['Classification'] = classifications.map(classify)

def quantify(classification):
    quantifications = {
        'Not reported': 0,
        'Inferred and uncertain': 1,
        'Inferred but nearly certain': 2,
        'Partially reported': 3,
        'Reported': 4
    }

    return quantifications[classification]

df['Score'] = df['Classification'].map(quantify)

df = df[['flags', 'Classification', 'Score', 'Summary']].sort_index(level=['Study', 'Category', 'Subcategory']) \
                                                        .reindex(['Common', 'Clinical stream', 'Cognitive-behavioral stream'], level=1) \
                                                        .reindex(orders, level=3)

df.to_excel('tmp/studies.xlsx')
out = df.reset_index(['Category', 'Subcategory'])[['Score', 'Summary']] \
        .fillna('') \
        .to_latex()
out = out.replace('tabular', 'longtable')
lines = out.splitlines()
print(lines[0])
open('tmp/studies.tex', 'w').write('\n'.join(lines[2:-1]))


df2 = df['Score'].unstack(['Category', 'Subcategory', 'Element'])
df2.to_excel('tmp/elements.xlsx')

out = df.reset_index().pivot('Study', 'Element', 'Score')[df.index.levels[3]].to_latex()
out = out.replace('tabular', 'longtable')

for element in categories.reset_index()['Element']:
    out = out.replace(element, '\\rot{%s}' % element, 1)

lines = out.splitlines()
print(lines[0])

open('tmp/elements.tex', 'w').write('\n'.join(lines[2:-1]))

df2 = df.reset_index().groupby(['Category', 'Subcategory', 'Element', 'Classification'])['Study'].count().unstack().fillna(0).applymap(np.int)\
                      .reindex(['Common', 'Clinical stream', 'Cognitive-behavioral stream'], level=0)\
                      .reindex(orders, level=2)
out = df2.to_latex()
for element in list(df2.columns):
    out = out.replace(element, '\\rot{%s}' % element, 1)

lines = out.splitlines()

print(lines[0])
open('tmp/classifications.tex', 'w').write('\n'.join(lines[2:-1]))
