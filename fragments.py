from sys import exit
from PyOrgMode import PyOrgMode
from pprint import pprint
import popplerqt4
import sys
import PyQt4
import textwrap
import yaml
import subprocess

def fragments(path):
    checklist = PyOrgMode.OrgDataStructure()
    checklist.load_from_file('elements.org')

    output = PyOrgMode.OrgDataStructure()
    output.root.append_clean('#+STARTUP: showall\n')

    pages = {}

    saved = open(path)
    for page_number, fragments in (yaml.load(saved) or {}).get('pages', {}).items():
        page = pages.setdefault(page_number, {})
        for fragment in fragments['fragments']:
            coords = tuple([tuple(c) for c in fragment['coords']])
            page[coords] = set(fragment['elements'].keys())

    source_path = "sources/%s.pdf" % path[8:-4]
    doc = popplerqt4.Poppler.Document.load(source_path)
    total_annotations = 0
    for i in range(doc.numPages()):
        #print("========= PAGE {} =========".format(i+1))
        page = doc.page(i)
        page_number = i + 1
        annotations = page.annotations()
        (pwidth, pheight) = (page.pageSize().width(), page.pageSize().height())
        if len(annotations) > 0:
            for annotation in annotations:
                if  isinstance(annotation, popplerqt4.Poppler.Annotation):
                    total_annotations += 1
                    if(isinstance(annotation, popplerqt4.Poppler.HighlightAnnotation)):
                        props = PyOrgMode.OrgDrawer.Element("PROPERTIES")
                        props.append(PyOrgMode.OrgDrawer.Property("PAGE", str(page_number)))

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
                            txt = txt + unicode(page.text(bdy)) + ' '

                            all_coords.append(tuple(int(coord) for coord in rect))
                            coords = str(all_coords[-1])[1:-1]
                            props.append(PyOrgMode.OrgDrawer.Property("COORDS", coords))

                        el = PyOrgMode.OrgNode.Element()
                        el.append_clean(props)

                        txt = txt.encode('utf8', 'replace')

                        el.heading = txt[:45].strip() + '...'

                        el.append_clean(textwrap.fill(txt, 80) + '\n\n')

                        def extract(root):
                            if type(root) is str:
                                return root

                            for i in range(root.level - 1):
                               el.append_clean('  ')

                            if all([type(node) is str for node in root.content]):
                                element = root.heading

                                el.append_clean('- ')

                                if element in pages.get(page_number, {}).get(tuple(all_coords), []):
                                    el.append_clean('[X]')
                                else:
                                    el.append_clean('[ ]')

                                el.append_clean(' %s\n' % element)
                            else:
                                el.append_clean('- %s [/]\n' % root.heading)

                            for node in root.content:
                                extract(node)

                        for node in checklist.root.content:
                            extract(node)

                        el.append_clean('#+LaTeX: \\newpage')
                        el.append_clean('\n\n')
                        output.root.append_clean(el)

    import tempfile
    with tempfile.NamedTemporaryFile(suffix='.org') as t:
        output.save_to_file(t.name)
        subprocess.call(['emacsclient', t.name])
        return t.read()
