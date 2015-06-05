#! /usr/bin/env python
# -*- coding: utf-8; -*-
#
# Copyright © 2014–2015 Émilien Tlapale
# Licensed under the Simplified BSD License

'''
reStructuredText support for bibgen.

Processing documents with citations and bibliographies is a three stage
process.

During the the first pass, the whole document is read, each citation
is marked as pending, and a ``bibliography`` directive is searched
for.  If no ``bibliography`` directive is found, the global
bibliography database present in settings is used. If it does not
exist, citations will not be resolved.

During the second pass, all citations initially found are looked up in
the bibliography database and registered. Then full bibliographic
entries are generated, if required, at the location of the
``.. bibliography::`` directive.

During the third and last pass, all citations are finally formatted,
and with references (links) to the bibliographic entries.
'''

from __future__ import absolute_import, print_function
import sys

import citeproc

import docutils.core
import docutils.nodes
import docutils.parsers.rst
import docutils.parsers.rst.roles

import bibgen


def parse_fragment(settings, text):
    '''Parse a generated reST fragment.'''
    # Get the parser
    parser = settings.rst_parser if \
             hasattr(settings, 'rst_parser') else \
             docutils.parsers.rst.Parser()
    # Create an empty document
    doc = docutils.utils.new_document('generated-bibliography')
    doc.settings.pep_references = 0
    doc.settings.rfc_references = 0
    doc.settings.tab_width = 8
    # Parse the rst fragment
    parser.parse(text, doc)
    return doc


class CitationSecondTransform(docutils.transforms.Transform):
    '''
    Docutils transform generating text for the registered citations.
    Citations are registered during a first pass occuring at node
    construction, but their text may need all the citations to be
    generated first, for instance for numbering.
    '''

    default_priority = 900

    def apply(self):
        raw_cit = self.startnode.details['raw_citation']
        cit = self.startnode.details['citation']
        biblio = self.startnode.details['biblio']

        def warn(cit_item):
            print('warning: citation reference not found for', cit_item.key,
                  file=sys.stderr)
        cit_txt = biblio.cite(cit, warn)

        nodes = []
        if sys.version_info >= (3, 0):
            txt = str(cit_txt)
        else:
            txt = unicode(cit_txt)

        nodes = []
        doc_item = parse_fragment(self.document.settings, txt)
        for child in doc_item.children[0].children:
            nodes.append(child)
            
        self.startnode.replace_self(nodes)

        
class CitationFirstTransform(docutils.transforms.Transform):
    default_priority = 700

    def apply(self):
        # Get the document biblio database
        biblio = self.document.settings.biblio
        
        # Get the citation keys
        raw_cit = self.startnode.details['raw_citation']
        keys = raw_cit.split(';')

        def link_format(key):
            return 'bib-'+key.lower()
        
        # Create a citation and register it
        def mkitem(key):
            return citeproc.CitationItem(key,
                                         prefix='`',
                                         suffix=' <#%s>`_'%link_format(key))
        cit = citeproc.Citation([mkitem(key) for key in keys])
        biblio.register(cit)

        # Create a new pending for the second transform
        pending = docutils.nodes.pending(CitationSecondTransform)
        pending.details['raw_citation'] = raw_cit
        pending.details['citation'] = cit
        pending.details['biblio'] = biblio
        self.document.note_pending(pending)

        self.startnode.replace_self(pending)

        #print('first transform of', self.startnode.details['raw_citation'],
        #      file=sys.stderr)
        
        
def cite_role(name, rawtext, text, lineno, inliner, options={}, content=[]):
    docutils.parsers.rst.roles.set_classes(options)

    # Create a citation
    
    # Create a pending transform to generate the reference
    # A transform is necessary to get a second pass, after numbering
    # and other first pass citation process has been performed
    pending = docutils.nodes.pending(CitationFirstTransform)
    pending.details['raw_citation'] = text
    inliner.document.note_pending(pending)

    #print('parsing cite for %s'%text, file=sys.stderr)

    # Container serving as position marker for the reference
    node = docutils.nodes.container()
    node.setup_child(pending)
    node += pending

    return node, []


class BibliographyTransform(docutils.transforms.Transform):
    default_priority = 800

    def apply(self):
        # Get the document biblio database
        biblio = self.startnode.details['biblio']
        sort = self.startnode.details['sort']
        hidden = self.startnode.details['hidden']

        # Done with the bibliography
        self.document.settings.biblio = None

        # Hidden bibliography directives show no entries
        if hidden:
            self.startnode.replace_self([])
            return

        # List cited references
        bib_entries = list(zip(biblio.items, biblio.bibliography()))
        if sort == 'alpha':
            bib_entries.sort(key=lambda x: x[0].key)

        def link_format(x):
            return 'bib-'+x.lower()

        nodes = []
        for (itm,bibitem) in bib_entries:
            text = ''.join(bibitem)
            doc_item = parse_fragment(self.document.settings, text)

            entry_node = docutils.nodes.paragraph('', classes=['bibentry'],
                                                  ids=[link_format(itm.key)])
            for child in doc_item.children:
                entry_node.setup_child(child)
                entry_node += child

            self.startnode.setup_child(entry_node)
            nodes.append(entry_node)

        self.startnode.replace_self(nodes)
        

class BibliographyDirective(docutils.parsers.rst.Directive):
    required_arguments = 0
    optional_arguments = 1
    # Allow long multi-line references to a biblio database
    final_argument_whitespace = True
    has_content = True
    option_spec = {'encoding': docutils.parsers.rst.directives.encoding,
                   'hidden': docutils.parsers.rst.directives.flag,
                   'mendeley': docutils.parsers.rst.directives.flag,
                   'sort': docutils.parsers.rst.directives.unchanged_required,
                   'style': docutils.parsers.rst.directives.unchanged_required}
    
    def run(self):
        #print('running the biblio directive', file=sys.stderr)
        #print('bibliography directive, content=', self.content, file=sys.stderr)

        # Get biblio database type
        db_type = 'bibtex'
        if 'mendeley' in self.options:
            db_type = 'mendeley'
            
        # Get biblio database
        if len(self.arguments) == 0:
            db_path = bibgen.default_database(db_type)
        else:
            db_path = self.arguments[0]

        # Other options
        hidden = 'hidden' in self.options
        style = self.options.get('style', 'harvard1')
        encoding = self.options.get('encoding', 'utf-8')
        sort = self.options.get('sort', 'alpha')

        # Open a biblio database for the document,
        # possibly replacing a command-line one.
        biblio = bibgen.open_bibliography(db_type, db_path,
                                          encoding, style, 'rst')

        # Create citations for the content
        if len(self.content) > 0:
            for key in self.content:
                itm = citeproc.CitationItem(key)
                cit = citeproc.Citation([itm])
                biblio.register(cit)
        # Only ibliography directives without content are citable
        else:
            self.state.document.settings.biblio = biblio

        pending = docutils.nodes.pending(BibliographyTransform)
        pending.details['biblio'] = biblio
        pending.details['hidden'] = hidden
        pending.details['sort'] = sort
        self.state.document.note_pending(pending)
        
        # The bibliography will be filled after the cite transforms
        node = docutils.nodes.container(classes=['bibliography'])
        node.setup_child(pending)
        node += pending

        return [node]

def register():
    docutils.parsers.rst.roles.register_canonical_role('cite', cite_role)
    docutils.parsers.rst.directives.register_directive('bibliography', BibliographyDirective)
    

def process_file(source, biblio, **kwds):
    if 'settings_overrides' in kwds:
        so = kwds['settings_overrides']
    else:
        so = {}
        kwds['settings_overrides'] = so
    so['biblio'] = biblio
    # Create a reST parser for generated content
    so['rst_parser'] = docutils.parsers.rst.Parser()
    # Parse and publish
    str = docutils.core.publish_string(source, **kwds)
    return str
