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

rows = []
for path in sys.argv[1:]:
    study = path[8:-4]
    fragments = yaml.load(open('fragments/%s.yml' % study))['pages']
    doc = popplerqt4.Poppler.Document.load(path)
    total_annotations = 0
    for i in range(doc.numPages()):
        #print("========= PAGE {} =========".format(i+1))
        page = doc.page(i)
        page_number = i + 1
        frags_page = fragments.get(page_number, {}).get('fragments', {})
        annotations = page.annotations()
        (pwidth, pheight) = (page.pageSize().width(), page.pageSize().height())
        if len(annotations) > 0:
            for annotation in annotations:
                if  isinstance(annotation, popplerqt4.Poppler.Annotation):
                    total_annotations += 1
                    if(isinstance(annotation, popplerqt4.Poppler.HighlightAnnotation)):
                        txt = ""
                        quads = annotation.highlightQuads()
                        all_coords = []
                        for quad in quads:
                            rect = (quad.points[0].x() * pwidth,
                                    quad.points[0].y() * pheight,
                                    quad.points[2].x() * pwidth,
                                    quad.points[2].y() * pheight)
                            bdy = PyQt4.QtCore.QRectF()
                            bdy.setCoords(*rect)
                            txt = txt + page.text(bdy) + ' '

                            all_coords.append(tuple(int(coord) for coord in rect))

                        all_coords = tuple(all_coords)

                        output = dict(Study=study,
                                      Page=page_number,
                                      Coordinates=all_coords,
                                      Text=txt.strip())

                        for fragment in frags_page:
                            if tuple((tuple(c) for c in fragment['coords'])) == all_coords:
                                for element in fragment['elements'].keys():
                                    output.update({element: 'x'})

                        rows.append(output)

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

df = pd.DataFrame(rows, columns=columns) \
       .set_index(['Study', 'Page', 'Coordinates'])

df.to_excel('/tmp/frags.xlsx')

print(yaml.safe_dump(df.drop('Text', 1).replace('\w', 1, regex=True).fillna(0).astype(int).reset_index().to_dict('records')))
