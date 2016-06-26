from sys import exit
from pprint import pprint
import popplerqt4
import sys
import PyQt4
import textwrap
import yaml
import pandas as pd
import numpy as np
import re
from ipdb import set_trace

colors_from_red = { 188: 'Green',
                    253: 'Red',
                    255: 'Yellow' }

path = sys.argv[1]
print(path)
doc = popplerqt4.Poppler.Document.load(path)
study = path[8:-4]
an = None
attributes = []
for i in range(doc.numPages()):
    page = doc.page(i)
    page_number = i + 1
    annotations = page.annotations()
    (pwidth, pheight) = (page.pageSize().width(), page.pageSize().height())
    if len(annotations) > 0:
        for annotation in annotations:
            if isinstance(annotation, popplerqt4.Poppler.TextAnnotation):
                an = annotation
                attribute, value = re.split(':\s+', an.contents())
                color = colors_from_red[an.style().color().red()]
                center = an.boundary().center()
                longitudinal = 'Top' if center.y() < 0.5 else 'Bottom'
                lateral = 'left' if center.x() < 0.5 else 'right'
                attributes.append(dict(Attribute=attribute,
                                       Value=value,
                                       Color=color,
                                       Location='%s %s' % (longitudinal, lateral),
                                       Page=page_number))

yaml.dump(attributes, open(sys.argv[2], 'w'))
