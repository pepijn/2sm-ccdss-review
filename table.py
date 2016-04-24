import yaml
import numpy
import pandas as pd
from pprint import pprint
import sys
from PyOrgMode import PyOrgMode

def categories(path):
    elements = PyOrgMode.OrgDataStructure()
    elements.load_from_file(path)

    # recursive; return ['Cognitive-behavioral flow', 'Presentation']

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
        result = dict(element=items.pop(len(items) - 1))
        stadia = ['category', 'subcategory']
        for stadium in stadia:
            try:
                result[stadium] = items.pop(0)
            except IndexError:
                result[stadium] = ' '
        return result

    return [tableize(element) for element in extract(elements.root)]

categories = categories('elements.org')
orders = []
for item in categories:
    orders.append(item['element'])
categories = pd.DataFrame(categories).set_index('element')
rows = []

for study_path in sys.argv[1:]:
    elements = yaml.load(open(study_path))['elements']

    study_name = study_path[9:-4]

    for element, data in elements.items():
        data.update(dict(study=study_name,
                         element=element))
        rows.append(data)

df = pd.DataFrame(rows) \
       .join(categories, on='element') \
       .set_index(['study', 'category', 'subcategory', 'element'])

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

df = df[['flags', 'classification', 'score', 'summary']].sort_index(level=['study', 'category', 'subcategory']) \
                                                        .reindex(['Common', 'Clinical stream', 'Cognitive-behavioral stream'], level=1) \
                                                        .reindex(orders, level=3)

df.to_excel('tmp/studies.xlsx')

df['score'].unstack(['category', 'subcategory', 'element']).to_excel('tmp/elements.xlsx')
