from sys import exit
from PyOrgMode import PyOrgMode
from pprint import pprint
import popplerqt4
import sys
import PyQt4
import textwrap
import yaml
import pandas as pd


elements = [
    'Decision-support system',
    'Trigger',

    'Patient',
    'Clinical knowledge',
    'Patient data',
    'Clinical conclusions',
    'Clinical advice',

    'User(s)',
    'Cognitive-behavioral knowledge',
    'User data',
    'Cognitive-behavioral conclusions',
    'Presentation'
]

df = pd.DataFrame(yaml.load(open('/tmp/elements.yml')))
texts = pd.read_pickle('/tmp/txt.pcl')
df['Coordinates'] = df['Coordinates'].map(lambda r: tuple((tuple(c) for c in r)))
df.set_index(['Study', 'Page', 'Coordinates'], inplace=True)

df = df.join(texts)

s = df.set_index('Text', append=True).stack()
s.index.names = s.index.names[:-1] + ['Element']
s = s[s > 0].reset_index('Text')['Text']
studies = s.reset_index()\
           .groupby(['Element', 'Study'])['Text']\
           .apply(lambda x: '\n\n'.join(x))\
           .unstack()\
           .fillna('')\
           .stack()\
           .to_frame()
studies.columns = ['Text']

dfs = {}
for element in elements:
    dfs[element] = studies.ix[element]

for path in sys.argv[1:]:
    study = path[9:-4]

    for element, attributes in yaml.load(open(path))['elements'].items():
        for attribute, value in attributes.items():
            dfs[element] = dfs[element].set_value(study, attribute, value)

with pd.ExcelWriter('/tmp/unit.xlsx') as writer:
    for element in elements:
        dfs[element].to_excel(writer, element[:31])
