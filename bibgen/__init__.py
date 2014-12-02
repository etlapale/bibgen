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

import importlib
import os
import os.path
import pathlib

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
      for path in pathlib.Path(d).glob('*@www.mendeley.com.sqlite'):
          return str(path)
    return None


def default_bibtex_database(doc):
    for d in [os.path.dirname(doc)]:
        for path in pathlib.Path(d).glob('*.bib'):
            return str(path)
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
