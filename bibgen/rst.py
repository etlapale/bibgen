#! /usr/bin/env python
# -*- coding: utf-8; -*-
#
# Copyright © 2014–2015 Émilien Tlapale
# Licensed under the Simplified BSD License

'''
reStructuredText support for bibgen.

Processing documents with citations and bibliographies is a three stage
process.

During the the first pass, the whole document is read, each
citation is registered, and a ``bibliography`` directive is searched for.
If no ``bibliography`` directive is found, the global bibliography
database present in settings is used. If it does not exist, citations
will not be resolved.

During the second pass, all citations initially found are looked up in
the bibliography database. During the third and last pass, all citations
are finally formatted, and the bibliography directive is printed, if
required.
'''

from __future__ import absolute_import, print_function
import sys

import citeproc

import docutils.core
import docutils.nodes
import docutils.parsers.rst
import docutils.parsers.rst.roles

import bibgen


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
            print('warning: citation reference not found for', cit_item.key)
        cit_txt = biblio.cite(cit, warn)

        #node = docutils.nodes.reference(raw_cit, cit_txt,
        #                                refuri='http://emilien.tlapale.com')
        node = docutils.nodes.Text(cit_txt)
        self.startnode.replace_self(node)
        print('second transform for', cit_txt, file=sys.stderr)

        
class CitationFirstTransform(docutils.transforms.Transform):
    default_priority = 700

    def apply(self):
        # Get the document biblio database
        biblio = self.document.settings.biblio
        
        # Get the citation keys
        raw_cit = self.startnode.details['raw_citation']
        keys = raw_cit.split(';')
        
        # Create a citation and register it
        def mkitem(key):
            return citeproc.CitationItem(key)
        cit = citeproc.Citation([mkitem(key) for key in keys])
        biblio.register(cit)

        # Create a new pending for the second transform
        pending = docutils.nodes.pending(CitationSecondTransform)
        pending.details['raw_citation'] = raw_cit
        pending.details['citation'] = cit
        pending.details['biblio'] = biblio
        self.document.note_pending(pending)

        self.startnode.replace_self(pending)

        print('first transform of', self.startnode.details['raw_citation'],
              file=sys.stderr)
        
        
def cite_role(name, rawtext, text, lineno, inliner, options={}, content=[]):
    docutils.parsers.rst.roles.set_classes(options)

    # Create a citation
    
    # Create a pending transform to generate the reference
    # A transform is necessary to get a second pass, after numbering
    # and other first pass citation process has been performed
    pending = docutils.nodes.pending(CitationFirstTransform)
    pending.details['raw_citation'] = text
    inliner.document.note_pending(pending)

    print('parsing cite for %s'%text, file=sys.stderr)

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

        # Create a bibliographic section
        sect = docutils.nodes.section(classes=['bibliography'])
        sect += docutils.nodes.title('', 'Bibliography')

        # List cited references
        bib_entries = list(zip(biblio.items, biblio.bibliography()))
        if sort == 'alpha':
            bib_entries.sort(key=lambda x: x[0].key)

        for (itm,bibitem) in bib_entries:
            entry_node = docutils.nodes.paragraph('', ''.join(bibitem))
            # TODO: Make biblio entries targetable
            #entry_node['refid'] = itm.key
            print(dir(entry_node))
            sect += entry_node
        
        self.startnode.replace_self(sect)

        print('bibliography transform', file=sys.stderr)
        

class BibliographyDirective(docutils.parsers.rst.Directive):
    required_arguments = 0
    optional_arguments = 1
    # Allow long multi-line references to a biblio database
    final_argument_whitespace = True
    has_content = False
    option_spec = {'encoding': docutils.parsers.rst.directives.encoding,
                   'mendeley': docutils.parsers.rst.directives.flag,
                   'style': docutils.parsers.rst.directives.unchanged}
    
    def run(self):
        print('running the biblio directive', file=sys.stderr)

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
        style = self.options.get('style', 'harvard1')
        encoding = self.options.get('encoding', 'utf-8')
        sort = self.options.get('sort', 'alpha')

        # Open a biblio database for the document,
        # possibly replacing a command-line one.
        biblio = bibgen.open_bibliography(db_type, db_path,
                                          encoding, style, 'rst')
        self.state.document.settings.biblio = biblio

        pending = docutils.nodes.pending(BibliographyTransform)
        pending.details['biblio'] = biblio
        pending.details['sort'] = sort
        self.state.document.note_pending(pending)
        
        # The bibliography will be filled after the cite transforms
        node = docutils.nodes.container()
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
    str = docutils.core.publish_string(source, **kwds)
    return str
