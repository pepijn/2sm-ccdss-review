from sys import exit
from PyOrgMode import PyOrgMode
from pprint import pprint
import popplerqt4
import sys
import PyQt4
import textwrap
import yaml
import pandas as pd
import numpy as np

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

columns = ['Study', 'Coordinates', 'Page', 'Text'] + elements

dfs = pd.read_excel(sys.argv[1], None)
df = pd.DataFrame()

for element, edf in dfs.items():
    edf.drop('Text', 1, inplace=True)
    edf['Element'] = element
    edf = edf.set_index(['Study', 'Element']).stack()
    edf.index.names = edf.index.names[:-1] + ['Attribute']

    if df.empty:
        df = edf
    else:
        df = df.append(edf)

for study in df.index.levels[0]:
    output = {}
    sdf = df[study]
    for element in sdf.index.levels[0]:
        if dict(sdf[element]):
            output[element] = dict(sdf[element])

    open('elements/%s.yml' % study, 'w').write(yaml.dump(dict(elements=output), default_flow_style=False))
