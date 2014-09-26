# Copyright © 2014  Émilien Tlapale
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import codecs
import os
import os.path
import pathlib
import xml.dom.minidom

import citeproc as cp
import citeproc.formatter

import bibgen.formatter

docbook_ns = 'http://docbook.org/ns/docbook'


def default_mendeley_database():
    '''
    Search for a default Mendeley sqlite database.
    '''
    # Linux
    dirs = [os.path.expanduser('~/.local/share/data/Mendeley Ltd./Mendeley Desktop')]
    # Windows Vista/7 (untested)
    if 'LOCALAPPDATA' in os.environ:
        dirs.append(os.path.join(os.environ('LOCALAPPDATA'),
                                 'Mendeley Ltd.', 'Mendeley Desktop'))
    # Windows XP (untested)
    dirs.append(os.path.join(os.path.expanduser('~'),
                             'Local Settings', 'Application Data',
                             'Mendeley Ltd.', 'Mendeley Desktop'))
    # MacOS X
    dirs.append(os.path.join(os.path.expanduser('~'),
                             'Library', 'Application Support',
                             'Mendeley Desktop'))
    
    for d in dirs:
      for path in pathlib.Path(d).glob('*@www.mendeley.com.sqlite'):
          return str(path)
    return None

def default_bibtex_database(doc):
    for d in [os.path.dirname(doc)]:
        for path in pathlib.Path(d).glob('*.bib'):
            return str(path)
    return None


def process_dom(dom, db_type='mendeley', db=None, db_encoding='utf-8',
                citation_separator=';', sort_order='alpha',
                style='harvard1',
                link_format=lambda x: x.lower()):
    '''
    mendeley, json and bibtex bibliography database are supported.
    
    :param xml.dom.Document dom:   Source DOM document.
    :param str db_type:            Bibliography database type.
    :param str db:                 Bibliography database.
    :param str db_encoding:        Bibliography database encoding.
    :param str citation_separator: Separator delimiting multiple citations
                                   in a single <citation/> element.
    :param str style:              CSL style to use.
    '''
    # Select a default bibliography database
    if db is None and db_type == 'mendeley':
        db = bibgen.default_mendeley_database()

    # Search all citations and their keys
    cit_nodes = [(n.childNodes[0].data.lower().split(citation_separator),n)
                 for n in dom.getElementsByTagNameNS(docbook_ns, 'citation') 
                 if len(n.childNodes) == 1
                    and n.childNodes[0].nodeType == n.TEXT_NODE]

    # Setup a citeproc context
    bib_style = cp.CitationStylesStyle(style)
    if db_type == 'mendeley':
        from bibgen.citeproc.mendeley import CiteProcMendeley
        bib_src = CiteProcMendeley(db)
    elif db_type == 'json':
        json_data = json.load(open(db))
        bib_src = citeproc.source.json.CiteProcJSON(json_data)
    # Default to BibTex
    else: 
        # Check for bibtexparser
        try:
            import bibtexparser
            with codecs.open(db, 'r', db_encoding) as fp:
                from bibgen.citeproc.bibtexparser import CiteProcBibTeX
                bib_src = CiteProcBibTeX(fp)
        # Use minimalistic bibtex parser from citeproc-py
        except ImportError:
            print('warning: defaulting to citeproc-py’s bibtex parser, you may want to install bibtexparser')
            with codecs.open(db, 'r', db_encoding) as fp:
                bib_src = citeproc.source.bibtex.BibTeX(fp)
    biblio = cp.CitationStylesBibliography(bib_style,
                                           bib_src, bibgen.formatter)

    # Create the citations
    cits = []
    for (keys,n) in cit_nodes:
        def mkitem(key):
            return cp.CitationItem(key,
                     prefix='<link linkend="%s">'%(link_format(key)),
                     suffix='</link>')
        cit = cp.Citation([mkitem(key) for key in keys])
        biblio.register(cit)
        cits.append(cit)

    # Print the citations
    def warn(cit_item):
        print('warning: citation reference not found for', cit_item.key)
    for ((keys,n),cit) in zip(cit_nodes,cits):
        txt = str(biblio.cite(cit,warn))
        cit_dom = xml.dom.minidom.parseString('<para>%s</para>'%txt)
        # Remove all previous <citation/> children
        for node in n.childNodes:
            n.removeChild(node)
        # Add the new children
        cit_root = cit_dom.documentElement
        while cit_root.hasChildNodes():
            n.appendChild(cit_root.firstChild)

    # Fill the existing bibliography node
    # TODO: add support for per-section bibliographies
    for bib_node in dom.getElementsByTagNameNS(docbook_ns, 'bibliography'):
        # Only keep the bibliography title
        # TODO: specify which nodes to keep
        for node in bib_node.childNodes:
            if node.nodeType == node.ELEMENT_NODE:
                if node.tagName != 'title':
                    bib_node.removeChild(node)
        # Add the bibliography entries
        bib_entries = list(zip(biblio.items,biblio.bibliography()))
        if sort_order == 'alpha':
            bib_entries.sort(key=lambda x: x[0].key)
        # TODO add support for raw entries
        for (itm,bibitem) in bib_entries:
            itemdom = xml.dom.minidom.parseString('<bibliomixed xml:id="%s">%s</bibliomixed>'%(link_format(itm.key),str(bibitem)))
            bib_node.appendChild(itemdom.documentElement)
        # Only process one bibliography element
        break
