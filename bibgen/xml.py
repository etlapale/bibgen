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
import xml.dom.minidom

import citeproc


docbook_ns = 'http://docbook.org/ns/docbook'


def process_dom(dom, biblio, citation_separator=';', sort_order='alpha',
                link_format=lambda x: x.lower()):
    '''
    :param xml.dom.Document dom:   Source DOM document.
    :param str citation_separator: Separator delimiting multiple citations
                                   in a single <citation/> element.
    '''
    # Search all citations and their keys
    cit_nodes = [(n.childNodes[0].data.lower().split(citation_separator),n)
                 for n in dom.getElementsByTagNameNS(docbook_ns, 'citation') 
                 if len(n.childNodes) == 1
                    and n.childNodes[0].nodeType == n.TEXT_NODE]

    # Create the citations
    cits = []
    for (keys,n) in cit_nodes:
        def mkitem(key):
            return citeproc.CitationItem(key,
                     prefix='<link linkend="%s">'%(link_format(key)),
                     suffix='</link>')
        cit = citeproc.Citation([mkitem(key) for key in keys])
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
