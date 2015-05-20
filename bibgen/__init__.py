# -*- coding: utf-8; -*-
#
# Copyright © 2014–2015 Émilien Tlapale
# Licensed under the Simplified BSD License

from __future__ import absolute_import, print_function

import glob
import importlib
import os
import os.path

import citeproc as cp


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
      for path in glob.iglob(os.path.join(d,'*@www.mendeley.com.sqlite')):
          return path
    return None


def default_bibtex_database(doc):
    for d in [os.path.dirname(doc)]:
        for path in glob.iglob(os.path.join(d, '*.bib')):
            return path
    return None

def default_database(db_type, doc_path=None):
    if db_type == 'mendeley':
        return default_mendeley_database()
    elif db_type == 'bibtex':
        return default_bibtex_database(doc_path)
    return None

def open_bibliography(db_type='mendeley', db=None, db_encoding='utf-8',
                      style='harvard1', formatter_name=None):
    '''
    :param str db_type:            Bibliography database type.
    :param str db:                 Bibliography database.
    :param str db_encoding:        Bibliography database encoding.
    :param str style:              CSL style to use.
    '''
    # Import the formatter
    if formatter_name is None:
        print('error: non formatter specified', file=sys.stderr)
        return None
    formatter = importlib.import_module('bibgen.formatter.'+formatter_name)

    # Select a default bibliography database
    if db is None and db_type == 'mendeley':
        db = bibgen.default_mendeley_database()

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
            print('warning: defaulting to citeproc-py’s bibtex parser, you may want to install bibtexparser', file=sys.stderr)
            with codecs.open(db, 'r', db_encoding) as fp:
                bib_src = citeproc.source.bibtex.BibTeX(fp)
    biblio = cp.CitationStylesBibliography(bib_style, bib_src, formatter)
    return biblio
