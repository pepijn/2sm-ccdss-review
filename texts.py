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

                        rows.append(output)

df = pd.DataFrame(rows) \
       .set_index(['Study', 'Page', 'Coordinates'])

df.to_pickle('/tmp/txt.pcl')
