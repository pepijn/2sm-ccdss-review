import yaml
import numpy
import pandas as pd
from pprint import pprint
import sys

rows = []

for study_path in sys.argv[1:]:
    elements = yaml.load(open(study_path))['elements']

    study_name = study_path[9:-4]

    for element, data in elements.items():
        data.update(dict(study=study_name,
                         element=element))
        rows.append(data)

df = pd.DataFrame(rows).set_index(['study', 'element'])

def classify(flags):
    classifications = {
        ('Reported', 'Not reported'): ['Partially reported']
    }

    return classifications.get(tuple(flags), flags)[0]

classifications = df['classification']
df['flags'] = classifications.map(lambda cs: ', '.join(cs))
df['classification'] = classifications.map(classify)

def quantify(classification):
    quantifications = {
        'Not reported': 0,
        'Inferred and uncertain': 1,
        'Inferred but nearly certain': 2,
        'Partially reported': 3,
        'Reported': 4
    }

    return quantifications[classification]

df['score'] = df['classification'].map(quantify)
df.to_excel('/tmp/ding.xls', columns=['flags', 'classification', 'score',
                                      'summary'])
